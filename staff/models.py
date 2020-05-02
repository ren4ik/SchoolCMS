import uuid

from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from phone_field import PhoneField
from pytils.translit import slugify

from handbook.models import EnglishLevel


class Teacher(models.Model):
	"""Модель учителя"""
	profile = models.OneToOneField(User, verbose_name="ссылка на профель", on_delete=models.CASCADE)
	group = models.CharField(Group, verbose_name="ссылка на группу", on_delete=models.CASCADE)
	first_name = models.CharField(verbose_name="Имя", max_length=20)
	last_name = models.CharField(verbose_name="Фамилия", max_length=20)
	father_name = models.CharField(verbose_name="Отчество", max_length=20)
	specialty = models.CharField(verbose_name="Специальность", max_length=20)
	birth_date = models.DateField(verbose_name="Дата рождения", auto_now=False, editable=True)
	hire_date = models.DateField(verbose_name="Дата приёма на работу", auto_now=False, editable=True)

	class EduLevel(models.IntegerChoices):
		SPECIAL = 1
		BACHELOR = 2
		MASTER = 3
		GRADUATE = 4
		PROFESSOR = 5

	edu_level = models.IntegerField(verbose_name="Уровень образования", choices=EduLevel.choices, default=1)
	diploma = models.CharField(verbose_name="Номер диплома", max_length=15)
	edu_location = models.CharField(verbose_name="ВУЗ/или др.", max_length=50)
	district = models.CharField(verbose_name="Район/Область", max_length=50)
	city = models.CharField(verbose_name="город", max_length=50)
	street = models.CharField(verbose_name="улица", max_length=50)
	home = models.CharField(verbose_name="дом", max_length=10)
	flat = models.PositiveSmallIntegerField(verbose_name="Квартира")
	work_experience = models.PositiveSmallIntegerField(verbose_name="Стаж работы")
	phone = PhoneField(blank=True, verbose_name="Телефон", help_text='Contact phone number')
	english_level = models.ForeignKey(EnglishLevel, verbose_name="Уровень владения анг.яз.", on_delete=models.CASCADE)
	is_staff = models.BooleanField(verbose_name="Сотрудник да/нет", default=False)
	is_curator = models.BooleanField(verbose_name="Куратор да/нет", default=False)
	is_manager = models.BooleanField(verbose_name="Менеджер да/нет", default=False)
	photo = models.ImageField(verbose_name="фото", upload_to="media/teacher/%Y/", default="", blank=True)
	slug = models.SlugField(verbose_name="url", max_length=10)
	number = models.UUIDField(
		unique=True,
		verbose_name="Уникальный номер",
		editable=False,
		auto_created=True,
		default=uuid.uuid4
	)

	class Meta:
		verbose_name = "Учитель"
		verbose_name_plural = "Учителя"

	def save(self, *args, **kwargs):
		d = f"{self.last_name}-{self.first_name}-{self.number}"
		self.slug = slugify(d)
		super(Teacher, self).save(*args, **kwargs)

	def __str__(self):
		return f"{self.last_name}-{self.first_name}-{self.number}"

	def get_absolute_url(self):
		return reverse('teacher', kwargs={'slug': self.slug})


class Curator(models.Model):
	"""Модель куратора"""
	pass


class Manager(models.Model):
	"""Модель управляющего"""
	pass
