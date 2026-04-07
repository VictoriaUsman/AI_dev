fig, axes = plt.subplots(3, 5, figsize=(15, 9))
axes = axes.flatten()

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']


for i in range(15):
    axes[i].imshow(images[i])
    label = labels[i]
    axes[i].set_title(f"Label: {label} ({class_names[label]})")
    axes[i].axis('off')


import matplotlib.pyplot as plt

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

fig, axes = plt.subplots(3, 5, figsize=(15, 9))
axes = axes.flatten()

for i in range(15):
    axes[i].imshow(images[i])
    label = labels[i]
    axes[i].set_title(f"Label: {label} ({class_names[label]})")
    axes[i].axis('off')

plt.tight_layout()
plt.show()
