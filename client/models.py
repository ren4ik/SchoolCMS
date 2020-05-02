from django.db import models
import uuid
from django.contrib.auth.models import User, Group
from django.urls import reverse
from phone_field import PhoneField
from pytils.translit import slugify
from django.utils import timezone

from handbook.models import EnglishLevel, Relationship


class Student(models.Model):
	profile = models.OneToOneField(User, verbose_name="ссылка на профель", on_delete=models.CASCADE)
	group = models.CharField(Group, verbose_name="ссылка на группу", default="student", on_delete=models.CASCADE)
	first_name = models.CharField(verbose_name="Имя", max_length=20)
	last_name = models.CharField(verbose_name="Фамилия", max_length=20)
	father_name = models.CharField(verbose_name="Отчество", max_length=20)
	birth_date = models.DateField(verbose_name="Дата рождения", auto_now=False, editable=True)
	hire_date = models.DateField(verbose_name="Дата приёма в школу", auto_now=False, editable=True)
	edu_last = models.CharField(verbose_name="школа до приёма", max_length=50)
	follower = models.BooleanField(verbose_name="С 1 класса", default=False)
	edu_experience = models.PositiveSmallIntegerField(verbose_name="Класс до приёма")
	phone = PhoneField(blank=True, verbose_name="Телефон", help_text='Contact phone number')
	english_level = models.ForeignKey(EnglishLevel, verbose_name="Уровень владения анг.яз.", on_delete=models.CASCADE)
	photo = models.ImageField(verbose_name="фото", upload_to="media/student/%Y/", default="", blank=True)
	slug = models.SlugField(verbose_name="url", max_length=10)
	number = models.UUIDField(
		unique=True,
		verbose_name="Уникальный номер",
		editable=False,
		auto_created=True,
		default=uuid.uuid4
	)

	class Meta:
		verbose_name = "Ученик"
		verbose_name_plural = "Ученики"

	def age_delta(self):
		self.age = timezone.now() - self.birth_date
		return self.age

	def save(self, *args, **kwargs):
		d = f"{self.last_name}-{self.first_name}-{self.number}"
		self.slug = slugify(d)
		super(Student, self).save(*args, **kwargs)

	def __str__(self):
		return f"{self.last_name}-{self.first_name}-{self.number}"

	def get_absolute_url(self):
		return reverse('student', kwargs={'slug': self.slug})


class Parent(models.Model):
	profile = models.OneToOneField(User, verbose_name="ссылка на профель", on_delete=models.CASCADE)
	group = models.CharField(Group, verbose_name="ссылка на группу", default="parent", on_delete=models.CASCADE)
	relationship = models.ForeignKey(Relationship, verbose_name="степень родства", on_delete=models.CASCADE)
	child = models.ForeignKey(Student, related_name="child", on_delete=models.CASCADE, verbose_name="имя ребёнка")
	is_active = models.BooleanField(verbose_name="Вкл/Выкл", default=False)
	first_name = models.CharField(verbose_name="Имя", max_length=20)
	last_name = models.CharField(verbose_name="Фамилия", max_length=20)
	father_name = models.CharField(verbose_name="Отчество", max_length=20)
	birth_date = models.DateField(verbose_name="Дата рождения", auto_now=False, editable=True)
	district = models.CharField(verbose_name="Район/Область", max_length=50)
	city = models.CharField(verbose_name="город", max_length=50)
	street = models.CharField(verbose_name="улица", max_length=50)
	home = models.CharField(verbose_name="дом", max_length=10)
	flat = models.PositiveSmallIntegerField(verbose_name="Квартира")
	phone = PhoneField(blank=True, verbose_name="Телефон", help_text='Contact phone number')
	english_level = models.ForeignKey(EnglishLevel, verbose_name="Уровень владения анг.яз.", on_delete=models.CASCADE)
	photo = models.ImageField(verbose_name="фото", upload_to="media/student/%Y/", default="", blank=True)
	slug = models.SlugField(verbose_name="url", max_length=10)
	number = models.UUIDField(
		unique=True,
		verbose_name="Уникальный номер",
		editable=False,
		auto_created=True,
		default=uuid.uuid4
	)

	class Meta:
		verbose_name = "Родитель/родственник"
		verbose_name_plural = "Родители/родственники"

	def save(self, *args, **kwargs):
		d = f"{self.last_name}-{self.first_name}-{self.number}"
		self.slug = slugify(d)
		super(Parent, self).save(*args, **kwargs)

	def __str__(self):
		return f"{self.last_name}-{self.first_name}-{self.number}"

	def get_absolute_url(self):
		return reverse('parent', kwargs={'slug': self.slug})
