import time
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# -----------------------------
# Step 1: Load processed dataset
# -----------------------------

X = np.load(r"D:\Green_GAN_CY\dataset\attack_features.npy")

# use subset
X = X[:20000]

print("Dataset loaded")
print("Dataset shape:", X.shape)

# convert to PyTorch tensor
X_tensor = torch.tensor(X, dtype=torch.float32)

# create dataset
dataset = TensorDataset(X_tensor)

# create dataloader
batch_size = 64
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

print("DataLoader ready")

print("Starting GAN training...")

# feature size
data_dim = X_tensor.shape[1]

# -----------------------------
# Step 2: Define Generator
# -----------------------------



class Generator(nn.Module):

    def __init__(self, noise_dim, data_dim):
        super(Generator, self).__init__()

        self.model = nn.Sequential(

            nn.Linear(noise_dim, 64),
            nn.ReLU(),

            nn.Linear(64, 128),
            nn.ReLU(),

            nn.Linear(128, data_dim),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.model(x)


# -----------------------------
# Step 3: Define Discriminator
# -----------------------------

class Discriminator(nn.Module):

    def __init__(self, data_dim):
        super(Discriminator, self).__init__()

        self.model = nn.Sequential(

            nn.Linear(data_dim, 256),
            nn.LeakyReLU(0.2),

            nn.Linear(256, 128),
            nn.LeakyReLU(0.2),

            nn.Linear(128, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.model(x)


# -----------------------------
# Step 4: Initialize Models
# -----------------------------

noise_dim = 100

generator = Generator(noise_dim, data_dim)
discriminator = Discriminator(data_dim)

# loss function
criterion = nn.BCELoss()

# optimizers
lr = 0.0002

optimizer_G = optim.Adam(generator.parameters(), lr=lr)
optimizer_D = optim.Adam(discriminator.parameters(), lr=lr)

start_time = time.time()

# -----------------------------
# Step 5: Training Loop
# -----------------------------

epochs = 40

for epoch in range(epochs):

    for batch in dataloader:

        real_data = batch[0]

        batch_size = real_data.size(0)

        # labels
        real_labels = torch.ones(batch_size, 1)
        fake_labels = torch.zeros(batch_size, 1)

        # -----------------------------
        # Train Discriminator
        # -----------------------------

        optimizer_D.zero_grad()

        # real data
        real_output = discriminator(real_data)
        loss_real = criterion(real_output, real_labels)

        # fake data
        noise = torch.randn(batch_size, noise_dim)
        fake_data = generator(noise)

        fake_output = discriminator(fake_data.detach())
        loss_fake = criterion(fake_output, fake_labels)

        loss_D = loss_real + loss_fake

        loss_D.backward()
        optimizer_D.step()

        # -----------------------------
        # Train Generator
        # -----------------------------

        optimizer_G.zero_grad()

        noise = torch.randn(batch_size, noise_dim)
        fake_data = generator(noise)

        output = discriminator(fake_data)

        loss_G = criterion(output, real_labels)

        loss_G.backward()
        optimizer_G.step()

    print(f"Epoch [{epoch+1}/{epochs}]  Loss_D: {loss_D.item():.4f}  Loss_G: {loss_G.item():.4f}")
    
print("\nTraining complete!")

end_time = time.time()
print("\nTraining Time:", end_time - start_time, "seconds")

# Save trained models
torch.save(generator.state_dict(), "generator.pth")
torch.save(discriminator.state_dict(), "discriminator.pth")

print("Models saved successfully!")