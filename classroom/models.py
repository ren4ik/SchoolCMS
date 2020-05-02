from django.db import models
from django.urls import reverse
from pytils.translit import slugify

from staff.models import Teacher
from handbook.models import Subject, TypeControl
from client.models import Student


class SubjectTeacher(models.Model):
	"""Связь предмета с учителем"""
	teacher = models.ForeignKey(
		Teacher,
		verbose_name="Учитель",
		on_delete=models.CASCADE,
		limit_choices_to={'is_staff': True},
	)
	subject = models.ForeignKey(Subject, verbose_name="Предмет", on_delete=models.CASCADE)
	is_active = models.BooleanField(verbose_name="ведёт да/нет", default=False)
	start_date = models.DateField(verbose_name="дата начала преподования", auto_now=False, editable=True)
	number_hours = models.PositiveSmallIntegerField(verbose_name="количество часов",)
	slug = models.SlugField(verbose_name="url", max_length=10)

	class Meta:
		verbose_name = "Связь учителя с предметом"
		verbose_name_plural = "Учителя и предметы"

	def save(self, *args, **kwargs):
		d = f"{self.teacher}-{self.subject}"
		self.slug = slugify(d)
		super(SubjectTeacher, self).save(*args, **kwargs)

	def __str__(self):
		return f"{self.teacher} / {self.subject}"

	def get_absolute_url(self):
		return reverse('teacher-subject', kwargs={'slug': self.slug})


class Mark(models.Model):
	"""Оценка знаний"""
	student = models.ForeignKey(
		Student,
		verbose_name="Ученик",
		on_delete=models.CASCADE,
		limit_choices_to={'is_active': True},
	)
	subject = models.ForeignKey(
		SubjectTeacher,
		verbose_name="Предмет",
		on_delete=models.CASCADE,
		limit_choices_to={'is_active': True},
	)
	issued_date = models.DateField(verbose_name="Фактическая дата выставления", auto_now=False, editable=True)
	recording_date = models.DateField(verbose_name="Дата ввода оценки", auto_now_add=True, editable=False)
	type_control = models.ForeignKey(TypeControl, verbose_name="Тип контроля", on_delete=models.CASCADE,)
	mark = models.PositiveSmallIntegerField(verbose_name="Оценка")
	slug = models.SlugField(verbose_name="url", max_length=10)

	class Meta:
		verbose_name = "Оценка"
		verbose_name_plural = "Оценки"

	def save(self, *args, **kwargs):
		d = f"{self.student}-{self.subject}-{self.mark}"
		self.slug = slugify(d)
		super(Mark, self).save(*args, **kwargs)

	def __str__(self):
		return f"{self.student}-{self.subject}-{self.mark}"

	def get_absolute_url(self):
		return reverse('mark', kwargs={'slug': self.slug})


class Point(models.Model):
	"""Балл ученика"""
	teacher = models.ForeignKey(
		Teacher,
		verbose_name="Учитель",
		on_delete=models.CASCADE,
		limit_choices_to={'is_active': True},
	)
	student = models.ForeignKey(
		Student,
		verbose_name="Ученик",
		on_delete=models.CASCADE,
		limit_choices_to={'is_active': True},
	)
	issued_date = models.DateField(verbose_name="Фактическая дата выставления", auto_now=False, editable=True)
	recording_date = models.DateField(verbose_name="Дата ввода балла", auto_now_add=True, editable=False)
	point = models.PositiveSmallIntegerField(verbose_name="Оценка")
	slug = models.SlugField(verbose_name="url", max_length=10)

	class Meta:
		verbose_name = "Оценка"
		verbose_name_plural = "Оценки"

	def save(self, *args, **kwargs):
		d = f"{self.student}-{self.point}"
		self.slug = slugify(d)
		super(Point, self).save(*args, **kwargs)

	def __str__(self):
		return f"{self.student}-{self.point}"

	def get_absolute_url(self):
		return reverse('point', kwargs={'slug': self.slug})


class ClassRoom(models.Model):
	pass
