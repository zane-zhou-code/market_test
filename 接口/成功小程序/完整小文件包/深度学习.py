import tensorflow as tf
# 定义一个随机量（标量）
random_float = tf.random.uniform(shape=())
print(random_float)
# 定义一个有2个元素的零向量
zero_vector = tf.zeros(shape=())
print(zero_vector)
# 定义两个2*2的常量矩阵
a = tf.constant([[1.,2.],[3.,4.]])
b = tf.constant([[5.,6.],[7.,8.]])
c = tf.add(a, b)
d = tf.matmul(a, b)
print(c)
print(d)

# 自动求导机制
x = tf.Variable(initial_value=3.)
with tf.GradientTape() as tape:  # 在 tf.GradientTape() 的上下文内，所有计算步骤都会被记录以用于求导
    y = tf.square(x)
y_grad = tape.gradient(y, x)   # 计算y关于x的导数
print([y, y_grad])

