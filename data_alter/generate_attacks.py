import torch
import torch.nn as nn
import numpy as np
import pandas as pd

# ----------------------------
# Generator Architecture
# ----------------------------

class Generator(nn.Module):
    def __init__(self, noise_dim, output_dim):
        super(Generator, self).__init__()

        self.model = nn.Sequential(
            nn.Linear(noise_dim, 128),
            nn.ReLU(),

            nn.Linear(128, 256),
            nn.ReLU(),

            nn.Linear(256, output_dim),
            nn.Tanh()
        )

    def forward(self, z):
        return self.model(z)


# ----------------------------
# Load trained generator
# ----------------------------


noise_dim = 100
data_dim = 78


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


generator = Generator(noise_dim, data_dim)

generator.load_state_dict(torch.load(r"D:\Green_GAN_CY\generator.pth"))

generator.eval()

print("Generator loaded successfully")

noise = torch.randn(1000, noise_dim)

fake_attacks = generator(noise).detach().numpy()

df = pd.DataFrame(fake_attacks)

df.to_csv("synthetic_attacks.csv", index=False)

print("Synthetic attacks generated:", len(df))


# ----------------------------
# Generate fake attack traffic
# ----------------------------
num_samples = 1000

noise = torch.randn(num_samples, noise_dim)

with torch.no_grad():
    synthetic_data = generator(noise).numpy()

print("Synthetic traffic generated:", synthetic_data.shape)

# ----------------------------
# Save synthetic data
# ----------------------------
df = pd.DataFrame(synthetic_data)

df.to_csv("synthetic_attacks.csv", index=False)

print("Saved to synthetic_attacks.csv")