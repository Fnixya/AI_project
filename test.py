import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Define universe of discourse
x = np.arange(0, 11, 1)

# Define fuzzy sets
y1 = fuzz.trimf(x, [0, 3, 6])  # Triangular membership function
y2 = fuzz.trimf(x, [4, 7, 10])  # Another triangular membership function

# Calculate fuzzy minimum

# Plot the fuzzy sets and their minimum
plt.figure()

# Plot fuzzy set 1
plt.plot(x, y1, 'b', linewidth=1.5, label='Fuzzy Set 1')

# Plot fuzzy set 2
plt.plot(x, y2, 'g', linewidth=1.5, label='Fuzzy Set 2')

# Plot fuzzy minimum
plt.plot(result[0], result[1], 'r', linewidth=2.5, label='Fuzzy Minimum')

plt.title('Fuzzy Sets and Fuzzy Minimum')
plt.xlabel('X')
plt.ylabel('Membership')
plt.legend()
plt.grid(True)
plt.show()
