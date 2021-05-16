from django.urls import path
from .views import *

app_name='storage'
urlpatterns = [
    path("", index, name="index"),
    path("obekti", listObekti.as_view(), name="obekt_list"),
    path("obekt/<int:pk>", detailObekti, name="obekt_detail"),
    path("obekt-nalichnost/<int:pk>", nalichnoObekt, name="obekt_nalichnost"),
    path("obekt/<int:pk>/update", updateObekt.as_view(), name="obekt_update"),
    path("obekt/<int:pk>/delete", deleteObekt.as_view(), name="obekt_delete"),
    path("create-obekt", createObekt.as_view(), name="obekt_form"),
    path("create-obekt-material", createMaterialObekt.as_view(), name="obekt_material_form"),
    path("update-obekt-material/<int:pk>", updateMaterialObekt.as_view(), name="obekt_material_update"),
    path("delete-obekt-material/<int:pk>", deleteMaterialObekt.as_view(), name="obekt_material_delete"),

    path("personal-type", listPersonalType, name="personal_type"),
    path("personal-type/<str:pk>", listPersonal, name="personal_list"),
    path("create-personal", createPersonal, name="personal_form"),
    path("personal/<int:pk>", detailPersonal.as_view(), name="personal_detail"),
    path("personal/<int:pk>/update", updatePersonal.as_view(), name="personal_update"),
    path("personal/<int:pk>/delete", deletePersonal.as_view(), name="personal_delete"),

    path("material-type", listMaterialType.as_view(), name="material_type_list"),
    path("create-material-type", createMaterialType.as_view(), name="material_type_create"),
    path("update-material-type/<int:pk>", updateMaterialType.as_view(), name="material_type_update"),
    path("delete-material-type/<int:pk>", deleteMaterialType.as_view(), name="material_type_delete"),

    path("material-type/<int:pk>", listMaterial, name="material_list"),
    path("material-type/<int:o_pk>/<int:m_pk>", listObektMaterial, name="obekt_material_list"),
    path("material/<int:pk>", detailMaterial, name="material_detail"),
    path("material/<int:pk>/update", updateMaterial.as_view(), name="material_update"),
    path("material/<int:pk>/delete", deleteMaterial.as_view(), name="material_delete"),
    path("create-material", createMaterial.as_view(), name="material_form"),

    path("machine", listMachine.as_view(), name="machine_list"),
    path("create-machine", createMachine.as_view(), name="machine_form"),
    path("machine/<int:pk>", detailMachine.as_view(), name="machine_detail"),
    path("machine/<int:pk>/update", updateMachine.as_view(), name="machine_update"),
    path("machine/<int:pk>/delete", deleteMachine.as_view(), name="machine_delete"),

    path("order-material", listOrderMaterial.as_view(), name="order_material_list"),
    path("create-order-material", createOrderMaterial.as_view(), name="order_material_create"),
    path("order-material/<int:pk>", detailOrderMaterial.as_view(), name="order_material_detail"),
    path("order-material-completed/<int:pk>", detailOrderMaterialCompleted.as_view(), name="order_material_completed_detail"),
    path("update-order-material/<int:pk>", updateOrderMaterial.as_view(), name="order_material_update"),
    path("delete-order-material/<int:pk>", deleteOrderMaterial.as_view(), name="order_material_delete"),

    path("create-order-machine", createOrderMachine.as_view(), name="order_machine_create"),
    path("order-machine", listOrderMachine.as_view(), name="order_machine_list"),
    path("order-machine/<int:pk>", detailOrderMachine.as_view(), name="order_machine_detail"),

]
