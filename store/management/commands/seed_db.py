from django.core.management.base import BaseCommand
from store.models import Category, Product, Review

class Command(BaseCommand):
    help = 'Seeds database with 30 initial products, categories, and sample reviews'

    def handle(self, *args, **options):
        self.stdout.write("Deleting old products & categories...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        categories_data = [
            {
                "name": "Audio & Wearables",
                "slug": "audio-wearables",
                "description": "High-fidelity spatial audio, active noise cancellation, and smart wearable tech.",
                "icon": "bi-headphones"
            },
            {
                "name": "Workstation & Tech",
                "slug": "workstation-tech",
                "description": "Ergonomic furniture, high-refresh displays, and mechanical desk accessories.",
                "icon": "bi-display"
            },
            {
                "name": "Smart Home & Living",
                "slug": "smart-home-living",
                "description": "Minimalist home decor, smart ambient lighting, and artisanal lifestyle goods.",
                "icon": "bi-house-heart"
            },
            {
                "name": "Lifestyle & Gear",
                "slug": "lifestyle-gear",
                "description": "Premium waterproof everyday carry, Merino wool apparel, and travel gear.",
                "icon": "bi-backpack"
            },
            {
                "name": "Gaming & Studio",
                "slug": "gaming-studio",
                "description": "Retro gaming gear, studio recording mics, and immersive spatial hardware.",
                "icon": "bi-controller"
            },
        ]

        created_categories = {}
        for cdata in categories_data:
            cat = Category.objects.create(**cdata)
            created_categories[cat.slug] = cat
            self.stdout.write(f"Created category: {cat.name}")

        products_data = [
            # Audio & Wearables
            {
                "name": "AuraSound Pro Wireless Headphones",
                "slug": "aurasound-pro-headphones",
                "category": created_categories["audio-wearables"],
                "price": 299.99,
                "old_price": 349.99,
                "description": "Experience uncompromised acoustics with adaptive active noise cancellation, 40-hour battery life, and spatial audio drivers calibrated by master sound engineers.",
                "short_specs": ["Active Noise Cancellation", "40-Hour Battery Life", "Custom 40mm Beryllium Drivers", "Ultra-soft Memory Foam"],
                "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80",
                "rating": 4.9,
                "review_count": 128,
                "stock": 18,
                "badge": "BESTSELLER",
                "tags": "wireless,audio,anc,bestseller",
                "is_featured": True
            },
            {
                "name": "Nova Earbuds Ultra",
                "slug": "nova-earbuds-ultra",
                "category": created_categories["audio-wearables"],
                "price": 149.99,
                "old_price": 179.99,
                "description": "Compact, powerful wireless earbuds with IPX7 waterproof rating, Hi-Res LDAC audio codec, and intuitive touch gesture controls.",
                "short_specs": ["IPX7 Waterproof", "Hi-Res LDAC Support", "28h Total Playtime with Case", "Dual Beamforming Mics"],
                "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=800&q=80",
                "rating": 4.7,
                "review_count": 85,
                "stock": 24,
                "badge": "HOT",
                "tags": "earbuds,wireless,waterproof,trending",
                "is_featured": True
            },
            {
                "name": "Pulse V2 Smart Spatial Watch",
                "slug": "pulse-v2-smartwatch",
                "category": created_categories["audio-wearables"],
                "price": 229.00,
                "old_price": None,
                "description": "Titanium alloy bezel smart watch featuring vibrant Always-On AMOLED screen, continuous ECG monitoring, blood oxygen telemetry, and 7-day battery endurance.",
                "short_specs": ["Titanium Alloy Case", "1.4\" AMOLED Display", "ECG + SpO2 Sensors", "5ATM Water Resistance"],
                "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
                "rating": 4.8,
                "review_count": 64,
                "stock": 12,
                "badge": "NEW",
                "tags": "smartwatch,fitness,health,new",
                "is_featured": True
            },
            {
                "name": "SonicBar Acoustic Soundbar",
                "slug": "sonicbar-acoustic-soundbar",
                "category": created_categories["audio-wearables"],
                "price": 199.50,
                "old_price": 249.00,
                "description": "Sleek low-profile home theater soundbar delivering 3D Dolby Atmos sound stage with wireless subwoofer support.",
                "short_specs": ["Dolby Atmos 3D", "HDMI eARC + Optical", "Bluetooth 5.3", "Integrated Subwoofer Pass-through"],
                "image": "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=800&q=80",
                "rating": 4.6,
                "review_count": 42,
                "stock": 8,
                "badge": "SALE",
                "tags": "audio,home,soundbar,speakers",
                "is_featured": False
            },
            {
                "name": "Vibe Studio Reference Headphones",
                "slug": "vibe-studio-headphones",
                "category": created_categories["audio-wearables"],
                "price": 189.99,
                "old_price": None,
                "description": "Flat-frequency studio monitor headphones engineered for sound mixing, audio editing, and pristine acoustic reproduction.",
                "short_specs": ["Neutral Sound Profile", "Detachable Braided Cable", "Open-back Acoustic Design", "Breathable Velour Pads"],
                "image": "https://images.unsplash.com/photo-1583394838336-acd977736f90?auto=format&fit=crop&w=800&q=80",
                "rating": 4.7,
                "review_count": 91,
                "stock": 15,
                "badge": None,
                "tags": "studio,monitoring,audio,pro",
                "is_featured": False
            },
            {
                "name": "Zenith Audio Smart Frames",
                "slug": "zenith-audio-smart-glasses",
                "category": created_categories["audio-wearables"],
                "price": 249.99,
                "old_price": 299.99,
                "description": "Revolutionary open-ear audio sunglasses with polarized UV400 lenses and directional speaker micro-arrays.",
                "short_specs": ["Polarized UV400 Lenses", "Open-Ear Directional Audio", "Hand-free Voice Assistant", "Lightweight TR-90 Frame"],
                "image": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?auto=format&fit=crop&w=800&q=80",
                "rating": 4.5,
                "review_count": 33,
                "stock": 5,
                "badge": "LIMITED",
                "tags": "smartwear,audio,eyewear,limited",
                "is_featured": False
            },

            # Workstation & Tech
            {
                "name": "Spectra 34\" Curved Ultrawide OLED Display",
                "slug": "spectra-34-curved-oled",
                "category": created_categories["workstation-tech"],
                "price": 899.99,
                "old_price": 1099.99,
                "description": "Ultra-immersive 175Hz 0.03ms response curved OLED monitor with DCI-P3 99% color gamut and USB-C 90W power delivery.",
                "short_specs": ["34\" 3440x1440 OLED", "175Hz Refresh / 0.03ms", "HDR True Black 400", "90W USB-C Pass-through"],
                "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=800&q=80",
                "rating": 4.95,
                "review_count": 210,
                "stock": 9,
                "badge": "BESTSELLER",
                "tags": "monitor,oled,ultrawide,gaming,workstation",
                "is_featured": True
            },
            {
                "name": "Apex Pro Custom Mechanical Keyboard",
                "slug": "apex-pro-mechanical-keyboard",
                "category": created_categories["workstation-tech"],
                "price": 179.99,
                "old_price": None,
                "description": "Gasket-mounted custom mechanical keyboard with hot-swappable tactile switches, double-shot PBT keycaps, and customizable RGB backlight.",
                "short_specs": ["Hot-Swappable Switches", "Gasket Mount Architecture", "South-facing RGB Lighting", "CNC Anodized Aluminum Top"],
                "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=80",
                "rating": 4.8,
                "review_count": 145,
                "stock": 22,
                "badge": "HOT",
                "tags": "keyboard,mechanical,rgb,workstation",
                "is_featured": True
            },
            {
                "name": "ErgoLift Electric Standing Desk Frame",
                "slug": "ergolift-electric-standing-desk",
                "category": created_categories["workstation-tech"],
                "price": 449.00,
                "old_price": 499.00,
                "description": "Dual-motor motorized sit-stand desk frame with whisper-quiet operation, anti-collision sensor, and 4 memory height presets.",
                "short_specs": ["Dual Motor Lift Mechanism", "350 lbs Weight Capacity", "4 Preset Memory Controller", "Whisper Quiet < 45dB"],
                "image": "https://images.unsplash.com/photo-1595515106969-1ce29566ff1c?auto=format&fit=crop&w=800&q=80",
                "rating": 4.7,
                "review_count": 78,
                "stock": 10,
                "badge": None,
                "tags": "furniture,standing-desk,ergonomic",
                "is_featured": False
            },
            {
                "name": "Lumino LED Task Lamp & Qi Charger",
                "slug": "lumino-led-task-lamp",
                "category": created_categories["workstation-tech"],
                "price": 79.99,
                "old_price": None,
                "description": "Architectural LED desk lamp with auto-brightness sensor, 5 color temperature modes, and integrated 15W wireless smartphone charger.",
                "short_specs": ["Auto-Dimming Light Sensor", "15W Qi Fast Wireless Charger", "5 Color Temps (2700K - 6500K)", "Touch Control Strip"],
                "image": "https://images.unsplash.com/photo-1534073828943-f801091bb18c?auto=format&fit=crop&w=800&q=80",
                "rating": 4.6,
                "review_count": 112,
                "stock": 35,
                "badge": "POPULAR",
                "tags": "lighting,desk,charger,tech",
                "is_featured": False
            },
            {
                "name": "Precision Wireless Ergonomic Mouse",
                "slug": "precision-wireless-mouse",
                "category": created_categories["workstation-tech"],
                "price": 89.99,
                "old_price": 109.99,
                "description": "Sculpted ergonomic wireless mouse featuring ultra-fast MagSpeed electromagnetic scrolling and an 8000 DPI track-anywhere optical sensor.",
                "short_specs": ["MagSpeed Electromagnetic Wheel", "8K DPI Track-Anywhere Sensor", "Multi-Device Bluetooth/2.4G", "70-Day USB-C Battery"],
                "image": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&w=800&q=80",
                "rating": 4.8,
                "review_count": 178,
                "stock": 30,
                "badge": "BESTSELLER",
                "tags": "mouse,ergonomic,wireless,productivity",
                "is_featured": False
            },
            {
                "name": "FlexiArm Heavy Duty Dual Monitor Mount",
                "slug": "flexiarm-dual-monitor-mount",
                "category": created_categories["workstation-tech"],
                "price": 119.99,
                "old_price": None,
                "description": "Gas spring dual monitor arm supporting monitors up to 32\" each, with full 360-degree rotation and integrated cable routing.",
                "short_specs": ["Holds up to 32\" Screens", "VESA 75x75 & 100x100 Compatible", "Gas Spring Height Adjustment", "Concealed Cable Pass"],
                "image": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&w=800&q=80",
                "rating": 4.7,
                "review_count": 52,
                "stock": 14,
                "badge": None,
                "tags": "monitor-arm,mount,desk,workstation",
                "is_featured": False
            },

            # Smart Home & Living
            {
                "name": "Aura Glow Ambient Light Bar Pair",
                "slug": "aura-glow-ambient-light-bar",
                "category": created_categories["smart-home-living"],
                "price": 129.99,
                "old_price": 149.99,
                "description": "Smart RGBIC light bars that dynamically sync color illumination to your music, movies, or gaming setups.",
                "short_specs": ["Screen & Audio Dynamic Sync", "16 Million RGBIC Colors", "Alexa & Google Assistant", "Desk Stand or TV Mount"],
                "image": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80",
                "rating": 4.85,
                "review_count": 94,
                "stock": 19,
                "badge": "HOT",
                "tags": "smart-home,rgb,lighting,ambience",
                "is_featured": True
            },
            {
                "name": "Nebula Ultrasonic Aroma Diffuser",
                "slug": "nebula-ultrasonic-diffuser",
                "category": created_categories["smart-home-living"],
                "price": 64.99,
                "old_price": None,
                "description": "Handcrafted ceramic ultrasonic mist diffuser with soft ambient warm glow lighting and safety auto-shutoff.",
                "short_specs": ["Handcrafted Ceramic Body", "Whisper Quiet Ultrasonic Atomizer", "Warm Mood Light Glow", "Auto Shutoff Safety Sensor"],
                "image": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?auto=format&fit=crop&w=800&q=80",
                "rating": 4.7,
                "review_count": 88,
                "stock": 40,
                "badge": "ECO",
                "tags": "home,diffuser,wellness,aromatherapy",
                "is_featured": False
            },
            {
                "name": "Artisan Precision Coffee Dripper Set",
                "slug": "artisan-coffee-dripper-set",
                "category": created_categories["smart-home-living"],
                "price": 84.50,
                "old_price": None,
                "description": "Hand-blown heat resistant borosilicate glass pour-over coffee carafe with reusable ultra-fine stainless steel mesh filter.",
                "short_specs": ["Borosilicate Heatproof Glass", "Dual-Layer Reusable Mesh Filter", "600ml / 20oz Capacity", "Ergonomic Walnut Handle"],
                "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=800&q=80",
                "rating": 4.9,
                "review_count": 130,
                "stock": 25,
                "badge": "BESTSELLER",
                "tags": "coffee,pourover,kitchen,artisan",
                "is_featured": True
            },
            {
                "name": "Puria HEPA Air Purifier Pro",
                "slug": "puria-hepa-air-purifier",
                "category": created_categories["smart-home-living"],
                "price": 219.00,
                "old_price": 269.00,
                "description": "Medical grade True HEPA H13 filtration system removing 99.97% of airborne allergens, dust, smoke, and odors.",
                "short_specs": ["True HEPA H13 Filter", "Real-time Air Quality Monitor", "Covers up to 500 sq. ft.", "22dB Night Sleep Mode"],
                "image": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?auto=format&fit=crop&w=800&q=80",
                "rating": 4.8,
                "review_count": 67,
                "stock": 11,
                "badge": "SALE",
                "tags": "air-purifier,home,health,clean-air",
                "is_featured": False
            },
            {
                "name": "Chronos E-Ink Minimalist Desk Clock",
                "slug": "chronos-eink-desk-clock",
                "category": created_categories["smart-home-living"],
                "price": 49.99,
                "old_price": None,
                "description": "High-contrast glanceable E-Ink digital desk clock equipped with precision temperature and ambient humidity sensors.",
                "short_specs": ["High Contrast E-Ink Screen", "Temperature & Humidity Sensors", "Magnetic Desk Stand", "1-Year Battery Life"],
                "image": "https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?auto=format&fit=crop&w=800&q=80",
                "rating": 4.5,
                "review_count": 49,
                "stock": 50,
                "badge": None,
                "tags": "clock,e-ink,minimalist,decor",
                "is_featured": False
            },
            {
                "name": "Hydra UV-C Smart Water Bottle 750ml",
                "slug": "hydra-uvc-smart-water-bottle",
                "category": created_categories["smart-home-living"],
                "price": 59.99,
                "old_price": None,
                "description": "Self-cleaning insulated water bottle equipped with built-in UV-C purification cap and digital water temperature indicator.",
                "short_specs": ["Integrated UV-C Purification", "24h Cold / 12h Hot Insulation", "Digital Cap Touch Screen", "BPA-Free Food Grade Steel"],
                "image": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=800&q=80",
                "rating": 4.6,
                "review_count": 73,
                "stock": 28,
                "badge": "NEW",
                "tags": "waterbottle,hydration,smart,wellness",
                "is_featured": False
            },

            # Lifestyle & Gear
            {
                "name": "AeroTech Waterproof Commuter Backpack 24L",
                "slug": "aerotech-waterproof-backpack",
                "category": created_categories["lifestyle-gear"],
                "price": 159.99,
                "old_price": 189.99,
                "description": "Ultra-durable Cordura ballistic nylon travel backpack featuring padded 16\" laptop chamber, hidden RFID security pocket, and weatherproof seal.",
                "short_specs": ["Cordura 1000D Waterproof Fabric", "Padded 16\" Laptop Sleeve", "RFID-Blocking Pocket", "Luggage Strap Pass-through"],
                "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=800&q=80",
                "rating": 4.9,
                "review_count": 162,
                "stock": 16,
                "badge": "BESTSELLER",
                "tags": "backpack,travel,waterproof,commuter",
                "is_featured": True
            },
            {
                "name": "Titan Minimalist Aluminum Card Wallet",
                "slug": "titan-minimalist-card-wallet",
                "category": created_categories["lifestyle-gear"],
                "price": 45.00,
                "old_price": None,
                "description": "RFID-blocking aerospace aluminum slim wallet with smooth mechanical trigger lever for instant single-handed card extraction.",
                "short_specs": ["Aerospace Grade Aluminum", "Holds up to 12 Cards", "Quick-Trigger Access Lever", "Integrated Cash Strap"],
                "image": "https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=800&q=80",
                "rating": 4.7,
                "review_count": 204,
                "stock": 60,
                "badge": "HOT",
                "tags": "wallet,rfid,edc,minimalist",
                "is_featured": True
            },
            {
                "name": "CloudSoft Merino Wool Tech Hoodie",
                "slug": "cloudsoft-merino-wool-hoodie",
                "category": created_categories["lifestyle-gear"],
                "price": 129.00,
                "old_price": None,
                "description": "Superfine 100% Australian Merino wool zip hoodie engineered for natural temperature regulation, odor resistance, and supreme softness.",
                "short_specs": ["100% Australian Merino Wool", "Natural Temperature Control", "Odor Resistant & Breathable", "Reinforced Thumbholes"],
                "image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&w=800&q=80",
                "rating": 4.8,
                "review_count": 89,
                "stock": 20,
                "badge": None,
                "tags": "apparel,hoodie,merino,wool",
                "is_featured": False
            },
            {
                "name": "Nomad Vacuum Thermal Tumbler 500ml",
                "slug": "nomad-thermal-travel-tumbler",
                "category": created_categories["lifestyle-gear"],
                "price": 39.99,
                "old_price": None,
                "description": "Double-wall stainless steel travel mug featuring 100% leak-proof magnetic slider lid and non-slip silicone base.",
                "short_specs": ["18/8 Stainless Steel", "Double-Wall Vacuum Insulation", "Magnetic Slider Lid", "Fits Standard Car Cupholders"],
                "image": "https://images.unsplash.com/photo-1577705998148-6da4f3963bc8?auto=format&fit=crop&w=800&q=80",
                "rating": 4.6,
                "review_count": 115,
                "stock": 45,
                "badge": None,
                "tags": "tumbler,drinkware,thermal,travel",
                "is_featured": False
            },
            {
                "name": "Luxe Leather Journal & Brass Pen Set",
                "slug": "luxe-leather-journal-pen-set",
                "category": created_categories["lifestyle-gear"],
                "price": 54.99,
                "old_price": None,
                "description": "Full-grain Italian leather refillable notebook cover paired with a solid weighted brass rollerball fountain-pen.",
                "short_specs": ["Full-Grain Italian Leather", "100gsm Acid-Free Cream Paper", "Solid Machined Brass Pen", "Refillable 240 Page Book"],
                "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=800&q=80",
                "rating": 4.8,
                "review_count": 56,
                "stock": 18,
                "badge": "GIFT",
                "tags": "journal,stationery,leather,gift",
                "is_featured": False
            },
            {
                "name": "Urban Shield Compact Anti-Theft Sling Bag",
                "slug": "urban-shield-anti-theft-sling",
                "category": created_categories["lifestyle-gear"],
                "price": 69.99,
                "old_price": 84.99,
                "description": "Ergonomic crossbody sling bag built with cut-proof fabric layer, lockable anti-theft zipper pullers, and external USB charging port.",
                "short_specs": ["Cut-Proof Kevlar Blend", "TSA Approved Cable Lock", "External USB Charging Port", "Water-Repellent Coating"],
                "image": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?auto=format&fit=crop&w=800&q=80",
                "rating": 4.7,
                "review_count": 98,
                "stock": 27,
                "badge": None,
                "tags": "slingbag,travel,security,edc",
                "is_featured": False
            },

            # Gaming & Studio
            {
                "name": "RetroCam X1 4K Digital Camera",
                "slug": "retrocam-x1-digital-camera",
                "category": created_categories["gaming-studio"],
                "price": 749.99,
                "old_price": 849.99,
                "description": "Vintage-inspired mirrorless digital camera combining classic tactile aluminum dials with modern 24MP APS-C sensor and 4K 60fps video recording.",
                "short_specs": ["24.2MP APS-C CMOS Sensor", "Classic Tactile Aluminum Dials", "4K 60fps / 1080p 120fps", "Built-in Wi-Fi & Bluetooth"],
                "image": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=800&q=80",
                "rating": 4.9,
                "review_count": 87,
                "stock": 6,
                "badge": "PREMIUM",
                "tags": "camera,retro,photography,4k",
                "is_featured": True
            },
            {
                "name": "PocketDeck OLED Handheld Gaming Console",
                "slug": "pocketdeck-oled-handheld-console",
                "category": created_categories["gaming-studio"],
                "price": 399.00,
                "old_price": None,
                "description": "Portable PC gaming handheld featuring a gorgeous 7\" HDR OLED touch display, custom 8-core APU, and tactile ergonomic thumbsticks.",
                "short_specs": ["7\" 120Hz OLED Touchscreen", "Custom 8-Core APU Architecture", "Hall-Effect Anti-Drift Joysticks", "High-Speed Wi-Fi 6E"],
                "image": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80",
                "rating": 4.85,
                "review_count": 140,
                "stock": 8,
                "badge": "HOT",
                "tags": "gaming,handheld,console,oled",
                "is_featured": True
            },
            {
                "name": "StudioCraft USB Studio Condenser Mic",
                "slug": "studiocraft-usb-condenser-mic",
                "category": created_categories["gaming-studio"],
                "price": 139.99,
                "old_price": 169.99,
                "description": "Broadcast-quality USB condenser microphone featuring 24-bit 96kHz audio resolution, dual polar patterns, and zero-latency headphone monitoring.",
                "short_specs": ["24-bit / 96kHz High-Res Audio", "Cardioid & Omnidirectional Switch", "Zero-Latency 3.5mm Output", "Heavy Duty Metal Stand"],
                "image": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=800&q=80",
                "rating": 4.7,
                "review_count": 105,
                "stock": 21,
                "badge": "POPULAR",
                "tags": "microphone,podcast,streaming,studio",
                "is_featured": False
            },
            {
                "name": "GamerCore Wireless Mechanical Arcade Stick",
                "slug": "gamercore-wireless-arcade-stick",
                "category": created_categories["gaming-studio"],
                "price": 169.99,
                "old_price": None,
                "description": "Tournament-grade fighting stick equipped with authentic Sanwa Denshi joystick & buttons, ultra-low latency 2.4G wireless, and magnetic lid access.",
                "short_specs": ["Sanwa Denshi Joystick & Buttons", "Ultra-Low Latency 2.4GHz Wireless", "Custom Macro Mapping", "40-Hour Rechargeable Battery"],
                "image": "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&w=800&q=80",
                "rating": 4.8,
                "review_count": 44,
                "stock": 13,
                "badge": None,
                "tags": "arcade,fightingstick,gaming,sanwa",
                "is_featured": False
            },
            {
                "name": "ProStream Monitor RGB Lightbar Dial",
                "slug": "prostream-monitor-rgb-lightbar",
                "category": created_categories["gaming-studio"],
                "price": 89.99,
                "old_price": None,
                "description": "Asymmetric optical monitor bar lighting up your desk surface without screen glare, complete with a wireless desktop control puck dial.",
                "short_specs": ["No-Screen-Glare Asymmetric Light", "Wireless Desktop Control Dial", "Backside Ambient RGB Glow", "RA95 High Color Accuracy"],
                "image": "https://images.unsplash.com/photo-1563089145-599997674d42?auto=format&fit=crop&w=800&q=80",
                "rating": 4.6,
                "review_count": 68,
                "stock": 32,
                "badge": None,
                "tags": "lightbar,desk,lighting,gaming",
                "is_featured": False
            },
            {
                "name": "VR-Pulse 4K Spatial Gaming Headset",
                "slug": "vr-pulse-4k-spatial-headset",
                "category": created_categories["gaming-studio"],
                "price": 549.99,
                "old_price": 629.99,
                "description": "Next-gen standalone VR headset featuring dual 4K Micro-OLED displays, pancake lenses, and optical hand-tracking camera array.",
                "short_specs": ["Dual 4K Micro-OLED Panels", "Advanced Optical Hand Tracking", "Compact Pancake Lens Optics", "Wireless PC Streaming Support"],
                "image": "https://images.unsplash.com/photo-1622979135225-d2ba269bc1bd?auto=format&fit=crop&w=800&q=80",
                "rating": 4.7,
                "review_count": 51,
                "stock": 4,
                "badge": "LIMITED",
                "tags": "vr,gaming,headset,spatial",
                "is_featured": False
            },
        ]

        sample_reviews = [
            ("Alex Mercer", 5, "Absolutely top tier build quality! The sound signature is crisp with punchy bass."),
            ("Elena Rostova", 5, "Fast shipping and packaging was ultra luxury. Exceeded my expectations."),
            ("David K.", 4, "Sleek aesthetic and works flawlessly. Highly recommended!"),
            ("Sarah Jenkins", 5, "Worth every single penny. Will definitely buy again from Lumina Store."),
        ]

        for pdata in products_data:
            p = Product.objects.create(**pdata)
            self.stdout.write(f"Created product #{p.id}: {p.name}")
            # Add 2 sample reviews for each product
            for author, r_rating, comment in sample_reviews[:2]:
                Review.objects.create(
                    product=p,
                    author=author,
                    rating=r_rating,
                    comment=comment
                )

        self.stdout.write(self.style.SUCCESS("Successfully seeded 30 products across 5 categories!"))
