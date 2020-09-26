# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree. An additional grant of patent rights
# can be found in the PATENTS file in the same directory.

import torch
from torch import nn
from torch.nn import Parameter
import torch.nn.functional as F

from fairseq import utils


class MultiheadAttention(nn.Module):
    """Multi-headed attention.

    See "Attention Is All You Need" for more details.
    """

    def __init__(self, embed_dim, num_heads, dropout=0., bias=True, add_bias_kv=False, add_zero_attn=False):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.dropout = dropout
        self.head_dim = embed_dim // num_heads
        assert self.head_dim * num_heads == self.embed_dim, "embed_dim must be divisible by num_heads"
        self.scaling = self.head_dim ** -0.5

        self.in_proj_weight = Parameter(torch.Tensor(3 * embed_dim, embed_dim))
        if bias:
            self.in_proj_bias = Parameter(torch.Tensor(3 * embed_dim))
        else:
            self.register_parameter('in_proj_bias', None)
        self.out_proj = nn.Linear(embed_dim, embed_dim, bias=bias)

        if add_bias_kv:
            self.bias_k = Parameter(torch.Tensor(1, 1, embed_dim))
            self.bias_v = Parameter(torch.Tensor(1, 1, embed_dim))
        else:
            self.bias_k = self.bias_v = None

        self.add_zero_attn = add_zero_attn

        self.reset_parameters()

        self.onnx_trace = False

    def prepare_for_onnx_export_(self):
        self.onnx_trace = True

    def reset_parameters(self):
        nn.init.xavier_uniform_(self.in_proj_weight)
        nn.init.xavier_uniform_(self.out_proj.weight)
        if self.in_proj_bias is not None:
            nn.init.constant_(self.in_proj_bias, 0.)
            nn.init.constant_(self.out_proj.bias, 0.)
        if self.bias_k is not None:
            nn.init.xavier_normal_(self.bias_k)
        if self.bias_v is not None:
            nn.init.xavier_normal_(self.bias_v)

    def forward(self, query, key, value, key_padding_mask=None, incremental_state=None,
                need_weights=True, static_kv=False, attn_mask=None):
        """Input shape: Time x Batch x Channel

        Self-attention can be implemented by passing in the same arguments for
        query, key and value. Timesteps can be masked by supplying a T x T mask in the
        `attn_mask` argument. Padding elements can be excluded from
        the key by passing a binary ByteTensor (`key_padding_mask`) with shape:
        batch x src_len, where padding elements are indicated by 1s.
        """

        # (NOTE) Self attn.
        qkv_same = query.data_ptr() == key.data_ptr() == value.data_ptr()
        # (NOTE) Enc-dec attn.
        kv_same = key.data_ptr() == value.data_ptr()

        # (NOTE) seq_len, batch_size, emb_dim.
        tgt_len, bsz, embed_dim = query.size()
        assert embed_dim == self.embed_dim
        assert list(query.size()) == [tgt_len, bsz, embed_dim]
        assert key.size() == value.size()

        if incremental_state is not None:
            saved_state = self._get_input_buffer(incremental_state)
            if 'prev_key' in saved_state:
                # previous time steps are cached - no need to recompute
                # key and value if they are static
                if static_kv:
                    assert kv_same and not qkv_same
                    key = value = None
        else:
            saved_state = None

        # (NOTE) q, k, v projection.
        if qkv_same:
            # self-attention
            # (NOTE)
            """
            OUT:
            `q`: len(Q) x B x emb(Q)  # alias: Q x B x QE
            `k`: len(K) x B x emb(K)  # alias: K x B x KE
            `v`: len(V) x B x emb(V)  # alias: V x B x VE
            """
            q, k, v = self.in_proj_qkv(query)
        elif kv_same:
            # encoder-decoder attention
            # (NOTE)
            """
            OUT:
            `q`: Q x B x QE
            `k`: K x B x KE
            `v`: V x B x VE
            """
            q = self.in_proj_q(query)
            if key is None:
                assert value is None
                k = v = None
            else:
                k, v = self.in_proj_kv(key)
        else:
            q = self.in_proj_q(query)
            k = self.in_proj_k(key)
            v = self.in_proj_v(value)

        # (NOTE) Scale.
        q *= self.scaling

        if self.bias_k is not None:
            assert self.bias_v is not None
            k = torch.cat([k, self.bias_k.repeat(1, bsz, 1)])
            v = torch.cat([v, self.bias_v.repeat(1, bsz, 1)])
            if attn_mask is not None:
                attn_mask = torch.cat([attn_mask, attn_mask.new_zeros(attn_mask.size(0), 1)], dim=1)
            if key_padding_mask is not None:
                key_padding_mask = torch.cat(
                    [key_padding_mask, key_padding_mask.new_zeros(key_padding_mask.size(0), 1)], dim=1)

        # (NOTE) Multi-heads.
        # (NOTE)
        """
        `q`: B * Head_Num x Q x Head_Dim  # alias: B * HN x Q x HD
        `k`: B * HN x K x HD
        `v`: B * HN x V x HD
        ===
        
        Basically the multi-head attn makes a sentence into 8 "sentences". Each "word" in the "sentence" has a dimension
        of 64.
        """
        q = q.contiguous().view(tgt_len, bsz * self.num_heads, self.head_dim).transpose(0, 1)
        if k is not None:
            k = k.contiguous().view(-1, bsz * self.num_heads, self.head_dim).transpose(0, 1)
        if v is not None:
            v = v.contiguous().view(-1, bsz * self.num_heads, self.head_dim).transpose(0, 1)

        if saved_state is not None:
            # saved states are stored with shape (bsz, num_heads, seq_len, head_dim)
            if 'prev_key' in saved_state:
                prev_key = saved_state['prev_key'].view(bsz * self.num_heads, -1, self.head_dim)
                if static_kv:
                    k = prev_key
                else:
                    k = torch.cat((prev_key, k), dim=1)
            if 'prev_value' in saved_state:
                prev_value = saved_state['prev_value'].view(bsz * self.num_heads, -1, self.head_dim)
                if static_kv:
                    v = prev_value
                else:
                    v = torch.cat((prev_value, v), dim=1)
            saved_state['prev_key'] = k.view(bsz, self.num_heads, -1, self.head_dim)
            saved_state['prev_value'] = v.view(bsz, self.num_heads, -1, self.head_dim)

            self._set_input_buffer(incremental_state, saved_state)

        src_len = k.size(1)

        if key_padding_mask is not None:
            assert key_padding_mask.size(0) == bsz
            assert key_padding_mask.size(1) == src_len

        if self.add_zero_attn:
            src_len += 1
            k = torch.cat([k, k.new_zeros((k.size(0), 1) + k.size()[2:])], dim=1)
            v = torch.cat([v, v.new_zeros((v.size(0), 1) + v.size()[2:])], dim=1)
            if attn_mask is not None:
                attn_mask = torch.cat([attn_mask, attn_mask.new_zeros(attn_mask.size(0), 1)], dim=1)
            if key_padding_mask is not None:
                key_padding_mask = torch.cat(
                    [key_padding_mask, torch.zeros(key_padding_mask.size(0), 1).type_as(key_padding_mask)], dim=1)

        # (NOTE) qv.
        # (NOTE)
        """
        IN:
        `q`: B * HN x Q x HD
        `k`: B * HN x K x HD
        
        OUT:
        `attn_weights`: B * HN x Q x K
        """
        attn_weights = torch.bmm(q, k.transpose(1, 2))
        assert list(attn_weights.size()) == [bsz * self.num_heads, tgt_len, src_len]

        # (NOTE) Attn mask.
        if attn_mask is not None:

            # (NOTE)
            """
            IN:
            `attn_mask`: T x T
            
            OUT:
            `attn_mask`: 1 x T x T
            """
            attn_mask = attn_mask.unsqueeze(0)

            if self.onnx_trace:
                attn_mask = attn_mask.repeat(attn_weights.size(0), 1, 1)

            # (NOTE)
            """
            The first 3 row of an example of `attn_weights`:
            
            [[ 3.5990e-01,        -inf,        -inf,        -inf,        -inf,
                -inf,        -inf,        -inf,        -inf,        -inf,
                -inf,        -inf,        -inf,        -inf,        -inf,
                -inf,        -inf,        -inf,        -inf,        -inf,
                -inf,        -inf,        -inf,        -inf,        -inf,
                -inf,        -inf,        -inf,        -inf,        -inf,
                -inf,        -inf,        -inf,        -inf,        -inf,
                -inf,        -inf,        -inf,        -inf,        -inf,
                -inf,        -inf,        -inf,        -inf,        -inf,
                -inf,        -inf,        -inf,        -inf,        -inf,
                -inf,        -inf,        -inf,        -inf,        -inf,
                -inf,        -inf,        -inf],
            [-4.4623e-01, -1.1409e+00,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf],
            [-2.6357e-01, -5.6254e-01,  1.3428e+00,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf,        -inf,        -inf,
                    -inf,        -inf,        -inf],
            """
            attn_weights += attn_mask

        # (NOTE) Pad mask.
        if key_padding_mask is not None:
            # don't attend to padding symbols
            attn_weights = attn_weights.view(bsz, self.num_heads, tgt_len, src_len)
            if self.onnx_trace:
                attn_weights = torch.where(
                    key_padding_mask.unsqueeze(1).unsqueeze(2),
                    torch.Tensor([float("-Inf")]),
                    attn_weights.float()
                ).type_as(attn_weights)
            else:

                # (NOTE)
                """
                First 3 rows of an example of `attn_weights`:
                
                [[[       -inf,        -inf,        -inf,        -inf,        -inf,
                 -inf,        -inf,        -inf,        -inf,  5.5486e-05,
                -5.3345e-05,  3.5280e-05,  7.8970e-06,  8.8221e-06,  2.4181e-05,
                -1.3521e-05,  8.7733e-05,  4.5073e-05,  9.6134e-05,  3.3491e-05,
                -1.1936e-06, -1.7224e-06,  5.3134e-05,  2.1350e-05,  8.2798e-05,
                -6.6834e-05, -1.2091e-05,  1.0418e-06,  2.6923e-05, -1.1653e-05,
                2.7246e-05,  3.1688e-05,  1.3204e-05, -7.0906e-05,  3.7103e-05,
                -1.5291e-05, -6.6240e-05, -6.3870e-05, -8.2717e-05, -3.8300e-05,
                -3.5043e-06, -8.5604e-05,  4.9391e-05, -4.5256e-05, -2.6180e-05,
                -2.1454e-05, -1.8675e-05, -3.4023e-05, -5.1459e-05, -1.1819e-05,
                4.7790e-05, -1.4592e-05,  2.0592e-05,  3.4617e-05, -2.3495e-05,
                -1.3083e-05, -3.9619e-05],
                [       -inf,        -inf,        -inf,        -inf,        -inf,
                     -inf,        -inf,        -inf,        -inf,  2.0088e-05,
                -2.7218e-05,  6.4722e-05,  4.6871e-05,  3.9172e-05,  6.6323e-05,
                -1.9273e-06,  4.3319e-05,  5.4963e-05,  9.3391e-05,  6.6103e-05,
                4.5571e-05,  1.1806e-05,  7.1448e-05,  1.9027e-05,  1.0273e-04,
                -1.1410e-04,  2.7014e-05,  1.3071e-05,  6.4876e-05,  1.7343e-05,
                2.1187e-05,  3.3326e-05,  6.8503e-05, -3.1598e-05,  2.5976e-06,
                -1.4918e-05, -3.3417e-05, -1.2936e-05, -3.9107e-05,  1.1284e-06,
                -2.2629e-05, -5.2664e-05,  3.3739e-05,  7.0486e-06,  2.8444e-06,
                -7.1802e-06, -1.4133e-05, -4.8211e-05, -3.3191e-05, -2.4902e-05,
                2.5068e-05,  4.0290e-05,  2.6975e-05,  6.0219e-05, -1.3715e-05,
                6.2488e-06,  1.0675e-05],
                [       -inf,        -inf,        -inf,        -inf,        -inf,
                     -inf,        -inf,        -inf,        -inf,  2.9379e-05,
                -2.5135e-05,  2.6368e-05, -1.2941e-05,  3.2903e-05, -1.5065e-05,
                -1.9264e-05,  4.4160e-05,  4.2562e-05,  7.7257e-05,  4.4542e-05,
                -8.0473e-06,  3.9488e-06,  4.8159e-05,  2.7119e-05,  6.2743e-05,
                -5.0461e-05, -1.6976e-06,  4.3061e-06,  4.6485e-05, -9.7562e-06,
                3.1080e-05,  1.6967e-05,  5.2871e-05, -3.0952e-05, -4.6637e-06,
                1.2257e-05, -5.8771e-05, -7.1945e-05, -3.9799e-05,  2.0061e-05,
                -1.3623e-05, -2.9724e-05,  2.7415e-05, -3.0823e-05, -1.5224e-05,
                -3.8755e-05,  4.1141e-05, -8.0822e-06, -5.4894e-05, -3.1128e-05,
                5.5890e-06, -1.5651e-05,  1.6181e-05,  1.2669e-05, -3.9055e-05,
                7.6929e-06, -3.7606e-05],
                """
                attn_weights = attn_weights.float().masked_fill(
                    key_padding_mask.unsqueeze(1).unsqueeze(2),
                    float('-inf'),
                ).type_as(attn_weights)  # FP16 support: cast to float and back
            attn_weights = attn_weights.view(bsz * self.num_heads, tgt_len, src_len)

        # (NOTE) Softmax. dim=-1: K.
        attn_weights = F.softmax(attn_weights.float(), dim=-1).type_as(attn_weights)
        attn_weights = F.dropout(attn_weights, p=self.dropout, training=self.training)

        # (NOTE) av.
        # (NOTE)
        """
        IN:
        `attn_weights`: B * HN x Q x K
        `v`: B * HN x V x HD
        
        OUT:
        `attn`: B * HN x Q x HD  # The same as `q`.
        """
        attn = torch.bmm(attn_weights, v)
        assert list(attn.size()) == [bsz * self.num_heads, tgt_len, self.head_dim]

        # (NOTE) Concat and lin.
        if (self.onnx_trace and attn.size(1) == 1):
            # when ONNX tracing a single decoder step (sequence length == 1)
            # the transpose is a no-op copy before view, thus unnecessary
            attn = attn.contiguous().view(tgt_len, bsz, embed_dim)
        else:
            attn = attn.transpose(0, 1).contiguous().view(tgt_len, bsz, embed_dim)
        attn = self.out_proj(attn)

        if need_weights:
            # average attention weights over heads
            attn_weights = attn_weights.view(bsz, self.num_heads, tgt_len, src_len)
            attn_weights = attn_weights.sum(dim=1) / self.num_heads
        else:
            attn_weights = None

        return attn, attn_weights

    def in_proj_qkv(self, query):
        return self._in_proj(query).chunk(3, dim=-1)

    def in_proj_kv(self, key):
        return self._in_proj(key, start=self.embed_dim).chunk(2, dim=-1)

    def in_proj_q(self, query):
        return self._in_proj(query, end=self.embed_dim)

    def in_proj_k(self, key):
        return self._in_proj(key, start=self.embed_dim, end=2 * self.embed_dim)

    def in_proj_v(self, value):
        return self._in_proj(value, start=2 * self.embed_dim)

    def _in_proj(self, input, start=0, end=None):
        weight = self.in_proj_weight
        bias = self.in_proj_bias
        weight = weight[start:end, :]
        if bias is not None:
            bias = bias[start:end]
        return F.linear(input, weight, bias)

    def reorder_incremental_state(self, incremental_state, new_order):
        """Reorder buffered internal state (for incremental generation)."""
        input_buffer = self._get_input_buffer(incremental_state)
        if input_buffer is not None:
            for k in input_buffer.keys():
                input_buffer[k] = input_buffer[k].index_select(0, new_order)
            self._set_input_buffer(incremental_state, input_buffer)

    def _get_input_buffer(self, incremental_state):
        return utils.get_incremental_state(
            self,
            incremental_state,
            'attn_state',
        ) or {}

    def _set_input_buffer(self, incremental_state, buffer):
        utils.set_incremental_state(
            self,
            incremental_state,
            'attn_state',
            buffer,
        )
