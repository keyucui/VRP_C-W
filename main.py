from vrp import *
from vrp_simple import SimVrp


if __name__ == '__main__':
	# 原节约法
	# vrp = Vrp()
	# vrp.start()

	# 稀疏图的改进节约法
	simVrp = SimVrp()
	simVrp.start()
