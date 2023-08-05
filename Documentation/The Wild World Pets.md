### Programmatic Architecture
Each creature is implemented as a class:
```Python
class Coraloin:
	def __init__(self):
		self.Name = "Coraloin"
		self.Nickname = None
		self.Health = 1500
		self.Hunger = 0
		self.Thirst = 0
		self.Relationships = {} #Entity:Score
		self.IsWild = Yes
		self.IsDomesticated = No
		self.IsPet = No
		self.Diet = {} #Item Name:Nourishing Provided

	def Eat(Item):
		if Item.Name in self.Diet:
			self.Hunger -= self.Diet[Item.Name]
		
	def Drink(Item):
		if Item.Name in self.Diet:
			self.Thirst -= self.Diet[Item.Name]
			
	def Pet(Player):
		self.Relationships[Player.Name] += 2 
```

### Brain Vomit

Pets are not used for goods, only for battles. When a pet dies, the fade away into dust. Creatures come from a monument with multiple doorways to our universe that lead to other universes full of their own life forms. 

Tiered pets caught using bait and enclosures that are crafted or bought. You can use a tier 1 bait on a water enclosure to catch specific types of creatures. 

### Enclosure Types
Nets
Aquatic nets
Cages
Special Enclosures

### Pet Actions
Can feed pets (pets can have specific diets)
Can play with pets
Can name pets
Can train pets
Can battle with pets

### Pet Needs
 - Happiness
 - Hunger
 - Relationship
 - Thirst

### Creature Types

Eclipseborn: Creatures born of eclipses, embodying the balance between light and shadow, with abilities influenced by celestial alignments. 

Nexillumin: Ancient beings connected to the cosmic nexus, they hold dominion over the pathways between realms. 

Xyrianthia: Etherial creatures residing in the gaps of reality, they possess the power to manipulate the boundaries of existence. 

Astroferns: Plant-like creatures with cosmic roots, harnessing energy from the stars and using it in symbiotic harmony. 

Nebuliths: Gaseous entities composed of stardust and cosmic gases, capable of morphing and reforming their bodies. 

Auroradons: Creatures akin to celestial dragons, they soar through the heavens, trailing radiant auroras in their wake. 

Omnitrons: Living constructs embodying the essence of multiple dimensions, they wield powers from parallel realities. 

Celestichors: Celestial steeds with constellations etched into their hides, they bear chosen riders through the cosmos. 

Voidforged: Entities born in the void, they possess abilities that draw on the abyssal powers of dark matter and anti-energy. 

Xenosplice: Creatures with bodies composed of multiple fragments, each part linked to a different cosmic plane. 

Etherechthys: Guardians of cosmic equilibrium, these beings maintain order and harmony throughout the universe. 

Eldrastrals: Eldritch beings that exist beyond mortal comprehension, influencing events on a cosmic scale. 

Elysium Envoys: Emissaries from the realm of Elysium, they bring knowledge of divine laws and cosmic wisdom.

Aeolusions: Creatures with the ability to control winds and air currents, guiding cosmic forces with their flight. 

Pyrradons: Legendary creatures born of ancient stars, holding the essence of cosmic fire and solar explosions

### Creatures
Coraloin - A creature with a nasty bite.
