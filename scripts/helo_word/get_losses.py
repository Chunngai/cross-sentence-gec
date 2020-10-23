import sys
import re

#log_file_path = sys.argv[1]

def get_losses(log_file_path):
    with open(log_file_path, encoding="utf-8") as log_file:
        lines = log_file.readlines()
    
    train_losses = []
    valid_losses = []
    
    train_losses_pattern = re.compile(r".*\| epoch (\d+?) \| loss (.*?) \|.*")
    valid_losses_pattern = re.compile(r".*\| epoch (\d+?) \| valid.* \| loss (.*?) \|.*")
    
    for line in lines:
        rst = valid_losses_pattern.match(line)
        if rst is not None:
            epoch_num = int(rst.group(1))
            valid_loss = float(rst.group(2))
    
            idx = epoch_num - 1
            try:
                valid_losses[idx].append(valid_loss)
            except IndexError:
                valid_losses.append([valid_loss])
        
        rst = train_losses_pattern.match(line)
        if rst is not None:
            epoch_num = int(rst.group(1))
            train_loss = float(rst.group(2))
    
            idx = epoch_num - 1
            try:
                train_losses[idx].append(valid_loss)
            except:
                train_losses.append([train_loss])
    
    for epoch_idx in range(len(train_losses)):
        loss_list = train_losses[epoch_idx]
    
        train_losses[epoch_idx] = sum(loss_list) / len(loss_list)
    
    for epoch_idx in range(len(valid_losses)):
        loss_list = valid_losses[epoch_idx]
    
        valid_losses[epoch_idx] = sum(loss_list) / len(loss_list)
    
    print(train_losses)
    print(valid_losses)

    return train_losses, valid_losses
