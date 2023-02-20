import yaml
from easy_dl import Config

# 加载配置的2种方式
# 1. 直接配置
# args = Config(
#     # 数据集
#     train_dir = './data/train',
#     valid_dir = './data/valid',
#
#     # 模型
#     latent_dim = 16,
#     channels = [512, 256, 128, 64, 32, 16, 16, 16],
#
#     # 训练过程
#     batch_size= 32,
#     lr= 0.001,
#
#     # 日志
#     logger_dir= './results',
#     running_name= 'default',
# )

# 2.从yaml文件加载
args = Config().load_yaml('./config.yaml', 'model1')

# 3. 与用户交互
# args.parse()


print(args)