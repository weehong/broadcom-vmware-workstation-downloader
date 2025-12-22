# broadcom-vmware-workstation-downloader

## Description
A software project designed to streamline the downloading of VMware Workstation software from Broadcom. This repository provides a set of scripts and tools to automate the process, ensuring that users have easy access to the latest versions.

## Features
- **Automated Downloading**: The `Scripts/download_software.py` script automates the process of downloading VMware Workstation software.
- **Shell Script**: The `download_vmware_workstation.sh` shell script provides an easy command-line interface for initiating downloads.
- **Docker Support**: Includes a `Dockerfile` to facilitate containerization of the downloading environment, ensuring consistency across different systems.
- **.gitignore**: Keeps the repository clean by excluding unnecessary files and directories.

## Installation Instructions
To set up the project on your local machine, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/weehong/broadcom-vmware-workstation-downloader.git
   cd broadcom-vmware-workstation-downloader
   ```

2. (Optional) Build and run with Docker:
   If you prefer to use Docker, build the image using the provided `Dockerfile`:
   ```bash
   docker build -t vmware-downloader .
   ```

## Usage Examples
### Using the Python Script
To download VMware Workstation using the Python script, run:
```bash
python Scripts/download_software.py
```

### Using the Shell Script
You can also initiate the download using the shell script:
```bash
bash download_vmware_workstation.sh
```

## Contributing Guidelines
We welcome contributions from the community! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

Please ensure that your code adheres to the project's coding standards and is well-documented.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
