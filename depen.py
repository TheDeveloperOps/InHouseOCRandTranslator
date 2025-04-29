from argostranslate import package, translate

# Update model index
package.update_package_index()

# Get available packages
available_packages = package.get_available_packages()

# Define required language pairs
required_pairs = [
    ("de", "en"),  # German → English
    ("ja", "en"),  # Japanese → English
    ("es", "en"),  # Spanish → English
    ("da", "en"),  # Danish → English
    ("pt", "en")   # Portuguese → English
]

# Install only required packages
for from_code, to_code in required_pairs:
    package_to_install = next((pkg for pkg in available_packages if pkg.from_code == from_code and pkg.to_code == to_code), None)
    if package_to_install:
        print(f"Downloading and installing model for {from_code} → {to_code}")
        package.install_from_path(package_to_install.download())
    else:
        print(f"⚠️ Model not found for {from_code} → {to_code}")

print("✅ Required translation models have been downloaded and installed.")
