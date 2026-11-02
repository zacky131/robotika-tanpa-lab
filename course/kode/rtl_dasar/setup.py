from setuptools import find_packages, setup

package_name = 'rtl_dasar'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    extras_require={'test': ['pytest']},
    zip_safe=True,
    maintainer="Muhammad Zacky Asy'ari",
    maintainer_email='zacky.asyari1986@gmail.com',
    description='Lab Robotika Tanpa Lab — contoh node dasar ROS 2 (Modul 2).',
    license='MIT',
    entry_points={
        'console_scripts': [
            'penerbit_halo = rtl_dasar.penerbit_halo:main',
            'pelanggan_halo = rtl_dasar.pelanggan_halo:main',
            'kura_persegi = rtl_dasar.kura_persegi:main',
            'kura_spiral = rtl_dasar.kura_spiral:main',
            'pemantau_kura = rtl_dasar.pemantau_kura:main',
        ],
    },
)
