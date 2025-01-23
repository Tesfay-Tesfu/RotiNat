from setuptools import setup, find_packages

setup(
    name="RotiNat",  
    version="0.0.3",  
    description="A package to calculate ROTI (Rate of TEC Index)",  
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",  
    author="Tesfay Tesfu", 
    author_email="tesfayphysics@gmail.com",  
    url="https://github.com/Tesfay-Tesfu/ROT_ROTI",  
    license="MIT",
    packages = find_packages(),
    install_requires=["pandas", "numpy","ipywidgets"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  
)
