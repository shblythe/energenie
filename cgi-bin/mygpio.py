import time,os,stat

class GPIO:
    _SYS_PATH="/sys/class/gpio"
    _EXPORT_FILE=_SYS_PATH+"/export"
    _UNEXPORT_FILE=_SYS_PATH+"/unexport"
    exported_channels=[]
    warnings=True

    @classmethod
    def _gpio_root_path(cls,channel):
        return cls._SYS_PATH+"/gpio"+str(channel)

    @classmethod
    def _gpio_dir_file(cls,channel):
        return cls._gpio_root_path(channel)+"/direction"

    @classmethod
    def _gpio_value_file(cls,channel):
        return cls._gpio_root_path(channel)+"/value"

    BCM=0
    BOARD=1
    mode=BCM
    @classmethod
    def setmode(cls,mode):
        if mode==cls.BOARD:
            raise ValueError('Not supported')
        cls.mode=mode

    @classmethod
    def setwarnings(cls,warnings):
        cls.warnings=warnings

    # direction
    OUT=0
    IN=1
    @classmethod
    def setup(cls,channel,direction,initial=0):
        cls.exported_channels.append(channel)
        try:
            with open(cls._EXPORT_FILE ,'r+') as f:
                f.write(str(channel))
        except IOError:
            if cls.warnings:
                print "Warning, pin ",channel," was in use already"
        # for some reason, this sometimes takes a while
        for attempt in range(10):
            try:
                with open(cls._gpio_dir_file(channel),'r+') as f:
                    f.write('in' if direction==cls.IN else 'out')
            except:
                time.sleep(0.05)
            else:
                break
        else:
            raise IOError("Couldn't set GPIO pin direction")
        if direction==GPIO.OUT:
            cls.output(channel,initial)

    @classmethod
    def input(cls,channel):
        with open(cls._gpio_value_file(channel),'r') as f:
            value=int(f.read(1))
        return value

    # state
    LOW=0
    HIGH=1
    @classmethod
    def output(cls,channel,state):
        if state==True:
            state=1
        if state==False:
            state=0
        with open(cls._gpio_value_file(channel),'r+') as f:
            f.write(str(state))

    @classmethod
    def cleanup(cls):
        for channel in cls.exported_channels:
            with open(cls._UNEXPORT_FILE,'r+') as f:
                f.write(str(channel))
        cls.exported_channels=[]

