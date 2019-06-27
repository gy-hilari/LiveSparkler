from __future__ import unicode_literals
from django.db import models
from ..login_app.models import User

class Message(models.Model):
    user = models.ForeignKey(User, related_name="message", null=True)

    message = models.CharField(max_length=280, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __repr__(self):
        return f"User: {self.user.first_name} {self.user.last_name}  |   Message = {self.message}"


################################################################################


class Firework(models.Model):
    name = models.CharField(max_length=45, null=True)
    rarity = models.IntegerField(null=True)

    def __repr__(self):
        return f"Firework#{self.id}: {self.name}  |   Rarity: {self.rarity}"

class FireworkInventory(models.Model):
    user = models.ForeignKey(User, related_name="user_fireworks")
    firework = models.ForeignKey(Firework, related_name="firework_users")

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __repr__(self):
        return f"Firework: {self.firework.name} in User: {self.user.first_name} {self.user.last_name}'s inventory, recieved at: {self.created_at}"


        # upon contribution of a firework to message, "trade-off"
            # FireworkInventory data with DeployedFirework, then delete the entry

class DeployedFirework(models.Model):
    # utilize this table to count total fireworks recieved for a user
        # message.recieved_fireworks.count in a for loop somewhere maybe
    message = models.ForeignKey(Message, related_name="recieved_fireworks", null=True)
    sent_by = models.ForeignKey(User, related_name="deployed_fireworks", null=True)
    firework = models.ForeignKey(Firework, related_name="deployments", null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __repr__(self):
        return f"Firework: {self.firework.name} deployed on message#{self.message.id} by user: {self.user.id} at {self.created_at}"


