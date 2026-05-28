import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/evang/projects/zefiro/Autopilot/zefiro_autonomy/install/zefiro_demo'
