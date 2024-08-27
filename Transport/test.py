class A:

	conf = {}
	intf = {}

	def __init__(self, arg1, b=None):

		if isinstance(arg1, A):
			self.copy_A(arg1)
		else:
			self.a = arg1
			self.b = b

	def copy_A(self, A):
		
		self.a = A.a
		self.b = A.b
		self.conf = A.conf
		self.intf = A.intf

x = A(1, 2)
x.conf["c"] = 3
x.intf["d"] = 4
print(x.a, x.b, x.conf, x.intf)

y = A(x)
print(y.a, y.b, y.conf, y.intf)