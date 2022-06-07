# all

This repository will hold all my Docker image repositories as subtrees. This way, I can run GitHub Actions that will check to see if any subtree image repositories have been updated - and if so, GitHub Actions can automatically rebuild the images, push them to Docker Hub, and rebuild any dependent images (and so on).
