import numpy as np
import matplotlib.pyplot as plt

save_file = "points_new.txt"

# Load data from text file
with open(save_file, 'r') as file:
    data = file.readlines()

def add_rows(matrix, row):
    if matrix.size == 0:
        return np.array(row).reshape(1, -1)
    else:
        return np.vstack((matrix, np.array(row)))

# Extract the coordinates
Rx = np.array([])
Ry = np.array([])
Px = np.array([])
Py = np.array([])

with open(save_file) as f:
    for line in set(f.readlines()):
        bot_coords, pixel_coords = eval(line)
        Rx = add_rows(Rx, [bot_coords[0]])
        Ry = add_rows(Ry, [bot_coords[1]])
        Px = add_rows(Px,[pixel_coords[0],1]) # - old using no rotation assumption
        Py = add_rows(Py,[pixel_coords[1],1]) # - old using no rotation assumption
print(Rx.size)

print(Px[:,0])


# old using no rotation assumption
m1, c1 = np.linalg.pinv(Px) @ Rx
m2, c2 = np.linalg.pinv(Py) @ Ry

m1, c1 = round(m1[0], 16), round(c1[0], 16)
m2, c2 = round(m2[0], 16), round(c2[0], 16)
print(f"m1,c1 = {m1},{c1}")
print(f"m2,c2 = {m2},{c2}")

# Create the figure and axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot the first set of points and line
ax1.plot(Px[:,0], Rx, 'bo', label='px,rx')
ax1.plot(Px, m1 * Px + c1, 'r-', label=f'f(x) = {m1:.2f}Px + {c1:.2f}')
ax1.set_xlabel('Px')
ax1.set_ylabel('Rx')
ax1.set_title('X Map and Line')
ax1.legend()
ax1.axis('equal')

# Plot the second set of points and line
ax2.plot(Py[:,0], Ry, 'go', label='py,ry')
ax2.plot(Py, m2 * Py + c2, 'r-', label=f'f(x) = {m2:.2f}x + {c2:.2f}')
ax2.set_xlabel('Py')
ax2.set_ylabel('Ry')
ax2.set_title('Y Map and Line')
ax2.legend()
ax2.axis('equal')

# Show the plot
plt.show()

# Save the plot
fig.savefig('G:/Projects/BlockPicking/assets/linear_regression_plt.png')
