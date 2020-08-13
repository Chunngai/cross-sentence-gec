### ！ **主要针对Ubuntu18.04和Ubuntu20.04.**

# 开始之前
## 1 基本配置
&emsp;&emsp;将ubuntu的默认shell从dash更改为bash：
```
# 备份原本的shell。
sudo cp /bin/sh /bin/sh.old
# 使sh指向bash。
sudo ln -fs /bin/bash /bin/sh
```

&emsp;&emsp;安装git和vim：
```
sudo apt update
sudo apt -y install git
sudo apt -y install vim
```

## 2 Python
### 2.1 安装Python3.6 **（针对非18.04的Ubuntu，如20.04。Ubuntu18.04跳过该步骤。其他系统如果python3默认是3.6也跳过该步骤）**  
```
# 安装依赖。
# 这两个依赖平常使用可能不用安装，但如果这里不安装，运行论文的源码会出错。
sudo apt install -y libbz2-dev
sudo apt install -y libsqlite3-dev

# 进入Downloads目录。
cd ~/Downloads

# 下载python3.6安装包。
wget https://www.python.org/ftp/python/3.6.11/Python-3.6.11.tgz
# 解压。
tar xzvf Python-3.6.11.tgz

# 进入安装包目录。
cd Python-3.6.11

# 安装。
./configure
sudo make
sudo make altinstall  # 与其他python版本共存
```

### 2.2 安装Python2.7 **（针对非18.04的Ubuntu，如20.04。Ubuntu18.04跳过该步骤。其他系统如果python2默认是2.7也跳过该步骤）**  
```
# 添加atom仓库。
echo "" | wget -qO - https://packagecloud.io/AtomEditor/atom/gpgkey | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] https://packagecloud.io/AtomEditor/atom/any/ any main" > /etc/apt/sources.list.d/atom.list'
sudo apt-get update

# 安装atom。
sudo apt-get -y install atom
```
&emsp;&emsp;以上命令实际上是通过安装atom间接安装python2.7。atom是github的一个文本编辑软件，其依赖包含python2.7。这种安装方式不容易出错。当然也可以通过其他方式安装python2.7，但会比较复杂，**特别是对于Ubuntu20.04**。

---

&emsp;&emsp;**非Ubuntu18.04**的系统按照上述操作安装python3和python2之后，在终端输入python3后显示的应该是系统原！本！的！python3版本；在终端输入python2后显示的应该是python2.7。

---

### 2.3 虚拟环境
&emsp;&emsp;虚拟环境提供一个与系统隔离的**python环境**。为了避免错误，**论文代码在虚拟环境运行**。

&emsp;&emsp;首先安装虚拟环境的依赖：
```
$ sudo apt -y install python3-venv
```

&emsp;&emsp;使用虚拟环境：
```
# 在当前目录创建一个名为gec的虚拟环境（其实就是一个目录）。
python3.6 -m venv gec  # 一定要是python3.6！！！虚拟环境名（此处为gec）可以不同。

# 激活虚拟环境。
source gec/bin/activate  # 该命令只有在虚拟环境文件夹（此处为gec）所在目录运行才成功。
# 如果在其他位置激活虚拟环境，则应运行: source [虚拟环境文件夹位置]/bin/activate
```

&emsp;&emsp;此时，终端提示符的开头会显示虚拟环境的名字。如果虚拟环境名为gec，应该显示:
```
(gec) [user]@[machine_name]: [path]$
```
&emsp;&emsp;其中，`[user]`为用户名，`[machine_name]`为机器名，`[path]`为当前路径，它们的具体值取决于用户的设置。

**注意：激活虚拟环境后，可以切换到任意目录，就像没使用虚拟环境那样。基本上，虚拟环境只用于存储python的安装包。**

---

**&emsp;&emsp;虚拟环境激活后，应满足前面的要求：  
&emsp;&emsp;1. 在终端输入`python`后，显示python3.6；  
&emsp;&emsp;2. 在终端输入`python2`后，显示python2.7。**

&emsp;&emsp;**如果以上两个要求不满足，运行论文的代码会出现问题！！！**

---

# 安装依赖
