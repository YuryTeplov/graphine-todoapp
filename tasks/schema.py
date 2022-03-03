import graphene
from graphene_django import DjangoObjectType
from .models import Task

STATUSES = ["later", "doing", "done"]

class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = ("id", "text", "status")

class DeleteTaskMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
    
    task = graphene.Field(TaskType)

    def mutate(self, info, id):
        task = Task.objects.get(pk=id)
        task.delete()

class CreateTaskMutation(graphene.Mutation):
    class Arguments:
        text = graphene.String(required = True)
        status = graphene.String(required = False)
    
    task = graphene.Field(TaskType)

    def mutate(self, info, text, status):
        if status in STATUSES:
            task = Task(text=text, status=status)
            task.save()
            return CreateTaskMutation(task=task)
        else:
            raise Exception('You can use only statuses from this list "later, doing, done"')



class EditTaskMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        text = graphene.String()
        status = graphene.String()

    task = graphene.Field(TaskType)

    def mutate(self, info, id, text, status):
        if status in STATUSES:
            task = Task.objects.get(pk=id)
            task.text = text
            task.status = status
            task.save()
            return EditTaskMutation(task=task)
        else:
            raise Exception('You can use only statuses from this list "later, doing, done"')




class Query(graphene.ObjectType):
    all_tasks = graphene.List(TaskType)

    def resolve_all_tasks(root, info):
        return Task.objects.all()

class Mutation(graphene.ObjectType):
    update_task = EditTaskMutation.Field()
    create_task = CreateTaskMutation.Field()
    delete_task = DeleteTaskMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
