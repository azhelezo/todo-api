from datetime import datetime, timedelta

from rest_framework.test import APITestCase

from tasks.models import Category, Tag, Task

TOMORROW = datetime.now() + timedelta(days=1)
NEXT_YEAR = datetime.now() + timedelta(days=365)


class TaskTests(APITestCase):

    def setUp(self):
        self.test_task = Task.objects.create(
            text='Test task',
            deadline=TOMORROW,
        )


class TestTasks(TaskTests):

    def test_task_view(self):
        response = self.client.get('/api/v1/tasks/')
        self.assertContains(response, self.test_task.text, status_code=200)

    def test_task_create(self):
        data = {'text': 'creation test', 'deadline': TOMORROW, }
        response = self.client.post('/api/v1/tasks/', data=data)
        self.assertContains(response, data.get('text'), status_code=201)
        response = self.client.get('/api/v1/tasks/')
        self.assertContains(response, data.get('text'), status_code=200)

    def test_task_update(self):
        pk = Task.objects.all().first().pk
        data = {
            'text': 'updated text',
            }
        response = self.client.patch(f'/api/v1/tasks/{pk}/', data=data)
        self.assertContains(response, data.get('text'), status_code=200)

    def test_task_delete(self):
        pk = Task.objects.all().first().pk
        response = self.client.delete(f'/api/v1/tasks/{pk}/')
        self.assertEquals(response.status_code, 204)
        response = self.client.get('/api/v1/tasks/')
        self.assertNotContains(response, self.test_task.text, status_code=200)


class TestTaskHistory(TaskTests):

    def test_task_history(self):
        pk = Task.objects.all().first().pk
        data = {'text': 'updated text', 'deadline': NEXT_YEAR, }
        response = self.client.put(f'/api/v1/tasks/{pk}/', data=data)
        self.assertContains(response, data.get('text'), status_code=200)
        response = self.client.get(f'/api/v1/tasks/{pk}/history/')
        self.assertContains(response, self.test_task.text, status_code=200)


class TestTags(TaskTests):

    def setUp(self):
        super().setUp()
        self.test_tag1 = Tag.objects.create(name='Tag1')
        self.test_tag2 = Tag.objects.create(name='Tag2')

    def test_tags_view(self):
        response = self.client.get('/api/v1/tags/')
        self.assertContains(response, self.test_tag1.name, status_code=200)

    def test_tag_create(self):
        data = {'name': 'Tag3', }
        response = self.client.post('/api/v1/tags/', data=data)
        self.assertContains(response, data.get('name'), status_code=201)
        response = self.client.get('/api/v1/tags/')
        self.assertContains(response, data.get('name'), status_code=200)

    def test_tag_update(self):
        tag = Tag.objects.all().first().name
        data = {'name': 'Tag4', }
        response = self.client.put(f'/api/v1/tags/{tag}/', data=data)
        self.assertContains(response, data.get('name'), status_code=200)

    def test_tag_delete(self):
        tag = Tag.objects.all().first().name
        response = self.client.delete(f'/api/v1/tags/{tag}/')
        self.assertEquals(response.status_code, 204)
        response = self.client.get('/api/v1/tags/')
        self.assertNotContains(response, tag, status_code=200)

    def test_tag_assign(self):
        pk = Task.objects.all().first().pk
        data = {
            'tags': [self.test_tag1, self.test_tag2, ]
        }
        response = self.client.patch(f'/api/v1/tasks/{pk}/', data=data)
        self.assertContains(response, data.get('tags')[0], status_code=200)
        task = Task.objects.get(pk=pk)
        response = self.client.get(f'/api/v1/tags/{self.test_tag1.name}/')
        self.assertContains(response, task.text, status_code=200)


class TestCategory(TaskTests):

    def setUp(self):
        super().setUp()
        self.test_cat1 = Category.objects.create(name='Category1')

    def test_categories_view(self):
        response = self.client.get('/api/v1/categories/')
        self.assertContains(response, self.test_cat1.name, status_code=200)

    def test_category_create(self):
        data = {'name': 'Category3', }
        response = self.client.post('/api/v1/categories/', data=data)
        self.assertContains(response, data.get('name'), status_code=201)
        response = self.client.get('/api/v1/categories/')
        self.assertContains(response, data.get('name'), status_code=200)

    def test_category_update(self):
        cat = Category.objects.all().first().name
        data = {'name': 'Category4', }
        response = self.client.put(f'/api/v1/categories/{cat}/', data=data)
        self.assertContains(response, data.get('name'), status_code=200)

    def test_category_delete(self):
        cat = Category.objects.all().first().name
        response = self.client.delete(f'/api/v1/categories/{cat}/')
        self.assertEquals(response.status_code, 204)
        response = self.client.get('/api/v1/categories/')
        self.assertNotContains(response, cat, status_code=200)

    def test_category_assign(self):
        pk = Task.objects.all().first().pk
        data = {
            'category': self.test_cat1,
        }
        response = self.client.patch(f'/api/v1/tasks/{pk}/', data=data)
        self.assertContains(response, data.get('category'), status_code=200)
        task = Task.objects.get(pk=pk)
        response = self.client.get(f'/api/v1/categories/{self.test_cat1}/')
        self.assertContains(response, task.text, status_code=200)


class TestDownload(TaskTests):

    def test_download_tasks(self):
        task_text = Task.objects.all().first().text
        response = self.client.get('/api/v1/tasks/download/')
        self.assertEquals(response.get('Content-Type'), 'text/csv')
        self.assertContains(response, task_text, status_code=200)

    def test_download_history(self):
        pk = Task.objects.all().first().pk
        task_text = Task.objects.get(pk=pk).text
        data = {
            'text': 'updated text',
            }
        response = self.client.patch(f'/api/v1/tasks/{pk}/', data=data)
        response = self.client.get(f'/api/v1/tasks/{pk}/history/download/')
        self.assertEquals(response.get('Content-Type'), 'text/csv')
        self.assertContains(response, task_text, status_code=200)


class TestUpload(TaskTests):

    def test_upload(self):
        response = self.client.post('/api/v1/tasks/send/')
        self.assertEquals(response.status_code, 200)
