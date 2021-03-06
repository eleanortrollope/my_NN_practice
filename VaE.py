from __future__ import print_function
import argparse 
import torch 
import torch.utils.data 
from torch import nn, optim 
from torch.nn import functional as F 
from torchvision import datasets, transforms 
from torchvision.utils import save_image 

# https://github.com/pytorch/examples/blob/master/vae/main.py 

class VAE(nn.Module):

  def __init__(self):
    super(VAE, self).__init__()

    self.fc1 = nn.Linear(784, 400)
    self.fc21 = nn.Linear(400, 20)
    self.fc22 = nn.Linear(400, 20)
    self.fc3 = nn.Linear(20, 400)
    self.fc4 = nn.Linear(400, 784)

  def encode(self, x):
    h1 = F.relu(self.fc1(x))
    return self.fc21(h1), self.fc22(h1)

  def reparameterize(self, mu, logvar):
    std = torch.exp(0.5 * logvar)
    eps = torch.randn_like(std)
    return mu + eps*std

  def decode(self, z):
    h3 = F.relu(self.fc3(z))
    return torch.sigmoid(self.fc4(h3))

  def forward(self, x):
    mu, logvar = self.encode(x.view(-1, 784))
    z = self.reparameterize(mu, logvar)
    return self.decode(z), mu, logvar 
  
parser = argparse.ArgumentParser(description='VAE MNIST example')
parser.add_argument('--batch-size', type=int, default=128, metavar='N',
                    help='input batch size for training (default: 128)')
parser.add_argument('--epochs', type=int, default=10, metavar='N', 
                    help='number of epochs to train (default: 10)')
parser.add_argument('--no-cuda', action='store_true', default=False, 
                   help='disables CUDA training')
parser.add_argument('--seed', type=int, default=10, metavar='N', 
                   help='random seed (default:1)')
parser.add_argument('--log-interval', type=int, default=10, metavar='N', 
                    help='how many batches to wait before logging training status')
args = parser.parse_args
  
