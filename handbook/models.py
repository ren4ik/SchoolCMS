from django.db import models
from django.urls import reverse
from pytils.translit import slugify


class SchoolLevel(models.Model):
	"""Primary schools, Junior Schools, Senior Schools"""
	name = models.CharField(verbose_name="уровень", max_length=100)
	slug = models.SlugField(verbose_name="url", max_length=100)
	photo = models.ImageField(verbose_name="фото", upload_to="media/school-level/", default="", blank=True)
	is_active = models.BooleanField(verbose_name="открыт", default=False)

	class Meta:
		verbose_name = "Уровень школы"
		verbose_name_plural = "Уровни школы"

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(SchoolLevel, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('school-level', kwargs={'slug': self.slug})


class Subject(models.Model):
	"""Предмет"""
	name = models.CharField(verbose_name="предмет", max_length=100)
	credit = models.PositiveSmallIntegerField(verbose_name="кредит предмета", default=0, blank=True)
	level = models.ForeignKey(SchoolLevel, verbose_name="уровень предмета", on_delete=models.CASCADE)
	# level_name = models.CharField(verbose_name="литера предмета", max_length=200, unique=True)
	slug = models.SlugField(verbose_name="url", max_length=100)
	photo = models.ImageField(verbose_name="фото", upload_to="media/subject/", default="", blank=True)
	is_active = models.BooleanField(verbose_name="активен", default=False)

	class Language(models.IntegerChoices):
		RU = 1
		EN = 2
		UZ = 3

	language = models.IntegerField(verbose_name="Язык обучения", choices=Language.choices, default=1)

	def save(self, *args, **kwargs):
		# self.level_name.upper = self.level + self.name
		name = self.name + ' ' + str(self.level) + ' ' + str(self.language)
		self.slug = slugify(name)
		super(Subject, self).save(*args, **kwargs)

	class Meta:
		verbose_name = "Предмет"
		verbose_name_plural = "Предметы"

	def __str__(self):
		return '%s / %s-%s' % (self.name, self.level, self.language)

	def get_absolute_url(self):
		return reverse('subject', kwargs={'slug': self.slug})


class Position(models.Model):
	"""Должность"""
	name = models.CharField(verbose_name="Должность", max_length=150)
	slug = models.SlugField(verbose_name="url", max_length=100)
	photo = models.ImageField(verbose_name="фото", upload_to="media/position/", default="", blank=True)
	is_active = models.BooleanField(verbose_name="открыта", default=False)

	class Meta:
		verbose_name = "Должность"
		verbose_name_plural = "Должности"

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Position, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('position', kwargs={'slug': self.slug})


class ClassCode(models.Model):
	"""Номер и литира класса (справочник)"""
	number = models.SmallIntegerField(verbose_name="Номер класса", unique=True)
	letter = models.CharField(verbose_name="литера класса", max_length=2)
	code = models.CharField(verbose_name="код класса", max_length=5)
	slug_name = models.SlugField(verbose_name="url", max_length=10)

	class Language(models.IntegerChoices):
		RU = 1
		EN = 2
		UZ = 3

	language = models.IntegerField(verbose_name="Язык обучения", choices=Language.choices, default=1)

	class Meta:
		verbose_name = "Код класса"
		verbose_name_plural = "Литеры классов"

	def save(self, *args, **kwargs):
		self.code = str(self.number) + ' ' + self.letter + ' ' + str(self.language)
		self.slug = slugify(self.code)
		super(ClassCode, self).save(*args, **kwargs)

	def __str__(self):
		return self.code

	def get_absolute_url(self):
		return reverse('class-code', kwargs={'slug': self.slug})


class BranchCode(models.Model):
	"""Филиалы"""
	name = models.CharField(verbose_name="имя филиала", max_length=100)
	city = models.CharField(verbose_name="город", max_length=50)
	street = models.CharField(verbose_name="улица", max_length=50)
	home = models.CharField(verbose_name="дом", max_length=10)
	rent = models.BooleanField(verbose_name="аренда", default=False)
	slug = models.SlugField(verbose_name="url", max_length=10)
	photo = models.ImageField(verbose_name="фото", upload_to="media/brunch/", default="", blank=True)
	is_active = models.BooleanField(verbose_name="открыт", default=False)

	class Meta:
		verbose_name = "Филиал"
		verbose_name_plural = "Филиалы"

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(BranchCode, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('branch-code', kwargs={'slug': self.slug})


class Club(models.Model):
	"""Клубы - внеклассная работа"""
	name = models.CharField(verbose_name="имя клуба", max_length=100)
	create_data = models.DateField(auto_now_add=True, verbose_name="дата открытия")
	level = models.ForeignKey(SchoolLevel, verbose_name="для кого?", on_delete=models.CASCADE)
	slug = models.SlugField(verbose_name="url", max_length=10)
	photo = models.ImageField(verbose_name="фото", upload_to="media/club/", default="", blank=True)
	is_active = models.BooleanField(verbose_name="открыт", default=False)

	class Language(models.IntegerChoices):
		RU = 1
		EN = 2
		UZ = 3

	language = models.IntegerField(verbose_name="Язык обучения", choices=Language.choices, default=1)

	class Meta:
		verbose_name = "Клуб"
		verbose_name_plural = "Клубы"

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Club, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('club', kwargs={'slug': self.slug})


class EnglishLevel(models.Model):
	"""Уровень владения английским"""
	level = models.CharField(verbose_name="уровень владения", max_length=20, unique=True)
	slug = models.SlugField(verbose_name="url", max_length=10)
	photo = models.ImageField(verbose_name="фото", upload_to="media/english-level/", default="", blank=True)
	is_active = models.BooleanField(verbose_name="открыт", default=False)

	class Meta:
		verbose_name = "Уровень английского"
		verbose_name_plural = "Уровени английского"

	def save(self, *args, **kwargs):
		level = self.level.upper
		self.slug = slugify(level)
		super(EnglishLevel, self).save(*args, **kwargs)

	def __str__(self):
		return self.level

	def get_absolute_url(self):
		return reverse('english-level', kwargs={'slug': self.slug})


class Relationship(models.Model):
	"""степень родства"""
	name = models.CharField(verbose_name="степень родства", max_length=50)
	slug = models.SlugField(verbose_name="url", max_length=10)

	class Meta:
		verbose_name = "Родитель/Родственник"
		verbose_name_plural = "Родители/Родственники"

	def save(self, *args, **kwargs):
		name = self.name.upper
		self.slug = slugify(name)
		super(Relationship, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('relationship', kwargs={'slug': self.slug})


class TypeControl(models.Model):
	"""Вид контроля справочник"""
	name = models.CharField(verbose_name="Вид контроля", max_length=50)
	slug = models.SlugField(verbose_name="url", max_length=10)

	class Meta:
		verbose_name = "Вид контроля"
		verbose_name_plural = "Виды контроля"

	def save(self, *args, **kwargs):
		name = self.name.upper
		self.slug = slugify(name)
		super(TypeControl, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('type-control', kwargs={'slug': self.slug})
