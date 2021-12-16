from easy_dl import config_setup,config_parse, strconfig, TensorboardLogger

if __name__ == '__main__':
    class Config:
        lr = 0.01
        batch_size=8
        num_epoch=100
        
    config = Config()
    config_parse(config)
    print(strconfig(config))

    logger = TensorboardLogger('./results','test')
    for i in range(1000,2000):
        logger.log_metric('quadratic', i**2, global_step=i)
        logger.log_metric('exponential', i**3, global_step=i)
        logger.log_metric('mse',i*4, global_step=i)