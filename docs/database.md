
# Tables

* users: id, name, password, email, permissions, created, modifed
* permissions: id, user_id, oikeus, checkpoint_id, created, modifed
* checkpoint: id, name, description, canBeVisible, location_id, created, modifed
* points: id, checkpoint_id, user_id, points, created, modifed
* location: id, locationData, checkpoint_id, created, modifed
