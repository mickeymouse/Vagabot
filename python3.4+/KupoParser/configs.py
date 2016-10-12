#This file contains the configurations required to parse some useful informations on ff14

Configs = { 
    'world' : 'Moogle', #world where we want to retrieve informations
    'ffxivURL' : 'http://fr.finalfantasyxiv.com', #official ffxiv website
    'worldstatusURL' : 'http://fr.finalfantasyxiv.com/lodestone/worldstatus', #worldstatus webpage
    'newsURL' : 'http://fr.finalfantasyxiv.com/lodestone/news/category/1', #webpage to get the news
    'charURL' : 'http://fr.finalfantasyxiv.com/lodestone/character/' #webpage to get info on characters
}

jobImgs = {
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/ec5d264e53ea7749d916d7d8bc235ec9c8bb7b51.png?1467272203' : 'Gladiateur',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/9fe08b7e2827a51fc216e6407646ffba716a44b8.png?1467272203' : 'Pugiliste',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/5ca476c2166b399e3ec92e8008544fdbea75b6a2.png?1467272203' : 'Maraudeur',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/924ded09293b2a04c4cd662afbf7cda7b0576888.png?1467272203' : 'Maître d\'hast',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/d39804e8810aa3d8e467b7a476d01965510c5d18.png?1467272203' : 'Archer',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/2d0ac2fdb4fd432d6b91acd7afbc335e87e877fb.png?1467272203' : 'Surineur',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/6157497a98f55a73af4c277f383d0a23551e9e98.png?1467272203' : 'Élémentaliste',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/e2a98c81ca279607fc1706e5e1b11bc08cac2578.png?1467272203' : 'Occultiste',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/59fde9fca303490477962039f6cd0d0101caeabe.png?1467272203' : 'Arcaniste',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/626a1a0927f7d2510a92558e8032831264110f26.png?1467272203' : 'Paladin',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/8873ffdf5f7c80770bc40f5b82ae1be6fa1f8305.png?1467272203' : 'Moine',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/2de279517a8de132f2faad4986a507ed728a067f.png?1467272203' : 'Guerrier',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/36ce9c4cc01581d4f900102cd51e09c60c3876a6.png?1467272203' : 'Chevalier dragon',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/7a72ef2dc1918f56e573dd28cffcec7e33a595df.png?1467272203' : 'Barde',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/1d4a1cf6021705ee62c5b5dfc100781f0f272623.png?1467272203' : 'Ninja',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/c460e288d5db83ebc90d0654bee6d0d0a0a9582d.png?1467272203' : 'Mage blanc',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/98d95dec1f321f111439032b64bc42b98c063f1b.png?1467272203' : 'Mage noir',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/2c38a1b928c88fd20bcc74fe0b4d9ba0a8f56f67.png?1467272203' : 'Invocateur',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/ee5788ae748ff28a503fecbec2a523dbc6875298.png?1467272203' : 'Érudit',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/a2a6213832a266f8c5145f7cbb8b8e8c9d8c6e25.png?1467272203' : 'Chevalier noir',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/2f21a984aab9ff20acc2cc9bcf0ffe544a33f3a1.png?1467272203' : 'Machiniste',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/970e5301281cba4ce374530f5949b74d7df083af.png?1467272203' : 'Astromancien',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/d41cb306af74bb5407bc74fa865e9207a5ce4899.png?1467272203' : 'Menuisier',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/6e0223f41a926eab7e6bc42af7dd29b915999db1.png?1467272203' : 'Forgeron',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/aab4391a4a5633684e1b93174713c1c52f791930.png?1467272203' : 'Armurier',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/605aa74019178eef7d8ba790b3db10ac8e9cd4ca.png?1467272203' : 'Orfèvre',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/f358b50ff0a1b1dcb67490ba8f4c480e01e4edd7.png?1467272203' : 'Tanneur',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/131b914b2be4563ec76b870d1fa44aa8da0f1ee6.png?1467272203' : 'Couturier',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/343bce834add76f5d714f33154d0c70e99d495a3.png?1467272203' : 'Alchimiste',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/86f1875ebc31f88eb917283665be128689a9669b.png?1467272203' : 'Cuisinier',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/8e82259fcd979378632cde0c9767c15dba3790af.png?1467272203' : 'Mineur',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/937d3313d9d7ef491319c38a4d4cde4035eb1ab3.png?1467272203' : 'Botaniste',
    'http://img.finalfantasyxiv.com/lds/pc/global/images/class/24/289dbc0b50956ce10a2195a75a22b500a648284e.png?1467272203' : 'Pêcheur'
}
