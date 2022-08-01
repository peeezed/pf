import irsdk

checkered        = 0x0001
white            = 0x0002
green            = 0x0004
yellow           = 0x0008
red              = 0x0010
blue             = 0x0020
debris           = 0x0040
crossed          = 0x0080
yellow_waving    = 0x0100
one_lap_to_green = 0x0200
green_held       = 0x0400
ten_to_go        = 0x0800
five_to_go       = 0x1000
random_waving    = 0x2000
caution          = 0x4000
caution_waving   = 0x8000
black      = 0x010000
disqualify = 0x020000
servicible = 0x040000 # car is allowed service (not a flag)
furled     = 0x080000
repair     = 0x100000


ir = irsdk.IRSDK()
ir.startup()


flag = ir["SessionFlags"]

if flag & repair:
    print("repair")

