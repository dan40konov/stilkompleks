from django.shortcuts import render
from django.http import HttpResponse
import requests
from api.models import *
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse_lazy
# Create your views here.
from api.forms import *
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

def index(request):
    ctx = {}
    if request.user.is_authenticated:
        personal = request.user.personal
        if (personal.position == 'De'):
            queryset = OrderMat.objects.filter(approved=True, complete=False).order_by('date')
        else:
            queryset = OrderMat.objects.filter(complete=False).order_by('date')
        ctx = { 'ordermat' : queryset }

    return render(request, 'storage/index.html', ctx)


'''def listObekti(request):
    response = requests.get('http://127.0.0.1:8000/api/obekti')
    obekti = response.json()

    ctx = {'obekti' : obekti}

    return render(request, 'storage/obekt_list.html', ctx)
'''
class listObekti(ListView):
    model = Obekti
    fields = ['name', 'investor', 'address', 'image']
    template_name = 'storage/obekt_list.html'


class createObekt(CreateView):
    model = Obekti
    fields = ['name', 'investor', 'address', 'image']
    template_name = 'storage/obekt_form.html'
    success_url = reverse_lazy('storage:obekt_list')

class updateObekt(UpdateView):
    model = Obekti
    fields = ['name', 'investor', 'address', 'image']
    template_name = 'storage/obekt_form.html'
    success_url = reverse_lazy('storage:obekt_list')

def detailObekti(request, pk):
    #response = requests.get('http://127.0.0.1:8000/api/obekti')
    #obekti = response.json()
    obekt = Obekti.objects.get(pk=pk)

    technicheski = ''

    if obekt.personal_set.exists:
        #r = requests.get('http://127.0.0.1:8000/api/personal')
        #personal = r.json()
        personal = Personal.objects.all()

        for p in personal:
            if p in obekt.personal_set.all() and p.position == 'Tc':
                technicheski = p.name


    orders = OrderMat.objects.filter(obekt=obekt)
    ctx = {'obekt' : obekt,'technicheski':technicheski, "orders": orders }

    return render(request, 'storage/obekt_detail.html', ctx)

def nalichnoObekt(request, pk):
    obekt = Obekti.objects.get(pk=pk)

    material_type = MaterialType.objects.all()
    ctx = {'obekt' : obekt, 'material_type':material_type}
    return render(request, 'storage/obekt_nalichnost.html', ctx)

def listObektMaterial(request, o_pk, m_pk):
    obekt = Obekti.objects.get(pk=o_pk)

    materials = [m for m in obekt.materialperobekt_set.filter(material__type=m_pk)]

    ctx = {'obekt' : obekt, 'material':materials}
    return render(request, 'storage/material_list_obekt.html', ctx)


def listPersonalType(request):
    personal_type = ['ТЕХНИЧЕСКИ РЪКОВОДИТЕЛИ', 'СНАБДИТЕЛИ И ШОФЬОРИ', 'АДМИНИСТРАТОРИ']

    ctx = {'personal_type': personal_type}

    return render(request, 'storage/personal_type.html', ctx)


def listPersonal(request, pk):
    #response = requests.get('http://127.0.0.1:8000/api/personal').json()
    response = Personal.objects.all()
    personal_type = {'1':'Tc', '2':'De', '3':'Ad'}
    personal_type_text = ['ТЕХНИЧЕСКИ РЪКОВОДИТЕЛИ', 'СНАБДИТЕЛИ И ШОФЬОРИ', 'АДМИНИСТРАТОРИ']
    personal = []
    for r in response:
        if r.position == personal_type[str(pk)]:
            personal.append(r)
    personal_type = personal_type_text[int(pk)-1]
    ctx = {'personal' : personal, 'personal_type':personal_type}

    return render(request, 'storage/personal.html', ctx)

#class createPersonal(CreateView):
#    model = Personal
#    fields = ['name', 'position', 'obekt', 'mail', 'phone_number', 'machine']
#    template_name = 'storage/material_form.html'
#    success_url = reverse_lazy('storage:personal_type')
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

def createPersonal(request):
    form_user = CreateUserFrom()
    form_personal = CreatePersonalForm()

    if request.method == 'POST':
        form_user = CreateUserFrom(request.POST)
        form_personal = CreatePersonalForm(request.POST)
        if form_user.is_valid() and form_personal.is_valid():

            user = form_user.save()
            personal = form_personal.save()
            obekt = request.POST.get('obekt')


            #after the user is created make the connection between user and personal
            personal.user = user
            personal.save()
            #if the user is set as admin add staff access to the user
            if request.POST.get('position') == 'Ad':
                u = User.objects.get(username=request.POST.get('username'))
                u.is_staff = True
                u.save()

            return redirect(reverse_lazy('storage:personal_type'))

    ctx = {'form_user':form_user,'form_personal':form_personal}
    return render(request, 'storage/personal_form.html', ctx)

class updatePersonal(UpdateView):
    model = Personal
    fields = ['name', 'position', 'obekt', 'mail', 'phone_number', 'machine', 'image']
    template_name = 'storage/material_form.html'
    success_url = reverse_lazy('storage:personal_type')



class detailPersonal(DetailView):
    model = Personal
    fields = ['name', 'position', 'obekt', 'mail', 'phone_number', 'machine', 'image']
    template_name = 'storage/personal_detail.html'


class listMaterialType(ListView):
    model = MaterialType
    fields = ['name']
    template_name = 'storage/material_type_list.html'


class createMaterialType(CreateView):
    model = MaterialType
    fields = ['name']
    template_name = 'storage/material_type_form.html'
    success_url = reverse_lazy('storage:material_type_list')


class updateMaterialType(UpdateView):
    model = MaterialType
    fields = ['name']
    template_name = 'storage/machine_form.html'
    success_url = reverse_lazy('storage:material_type_list')


class deleteMaterialType(DeleteView):
    model = MaterialType
    success_url = reverse_lazy('storage:material_type_list')
    template_name = 'storage/material_type_delete.html'


def listMaterial(request, pk):
    material_type = MaterialType.objects.get(pk=pk)
    materials = Material.objects.filter(type=pk)

    ctx = {'material' : materials, 'material_type' : material_type}

    return render(request, 'storage/material_list.html', ctx)


def detailMaterial(request, pk):
    material = Material.objects.get(pk=pk)
    material_per_obekt = MaterialPerObekt.objects.filter(material=material)
    print(material_per_obekt)
    ctx = {'material': material, 'material_per_obekt':material_per_obekt}

    return render(request, 'storage/material_detail.html', ctx)


class createMaterial(CreateView):
    model = Material
    fields = ['name', 'type', 'description', 'amount_type', 'image']
    template_name = 'storage/material_form.html'
    success_url = reverse_lazy('storage:material_type_list')


class updateMaterial(UpdateView):
    model = Material
    fields = ['name', 'type', 'description', 'amount_type', 'image']
    template_name = 'storage/material_form.html'
    success_url = reverse_lazy('storage:material_type_list')


class listMachine(ListView):
    model = Machine
    fields = ['name', 'description', 'image']
    template_name = 'storage/machine_list.html'


class detailMachine(DetailView):
    model = Machine
    fields = ['name', 'description', 'image']
    template_name = 'storage/machine_detail.html'


class createMachine(CreateView):
    model = Machine
    fields = ['name', 'description', 'image']
    template_name = 'storage/machine_form.html'
    success_url = reverse_lazy('storage:machine_list')


class updateMachine(UpdateView):
    model = Machine
    fields = ['name', 'description', 'image']
    template_name = 'storage/machine_form.html'
    success_url = reverse_lazy('storage:machine_list')


class deleteMachine(DeleteView):
    model = Machine
    success_url = reverse_lazy('storage:machine_list')
    template_name = 'storage/machine_delete.html'


class deleteObekt(DeleteView):
    model = Obekti
    success_url = reverse_lazy('storage:obekt_list')
    template_name = 'storage/obekt_delete.html'


class deletePersonal(DeleteView):
    model = Personal
    success_url = reverse_lazy('storage:personal_type')
    template_name = 'storage/personal_delete.html'


class deleteMaterial(DeleteView):
    model = Material
    success_url = reverse_lazy('storage:material_type_list')
    template_name = 'storage/material_delete.html'



class createMaterialObekt(CreateView):
    model = MaterialPerObekt
    fields = ['obekt', 'material', 'amount']
    template_name = 'storage/obekt_material_form.html'
    success_url = reverse_lazy('storage:obekt_list')

class updateMaterialObekt(UpdateView):
    model = MaterialPerObekt
    fields = ['obekt', 'material', 'amount']
    template_name = 'storage/obekt_material_form.html'
    success_url = reverse_lazy('storage:obekt_list')

class deleteMaterialObekt(DeleteView):
    model = MaterialPerObekt
    template_name = 'storage/obekt_material_delete.html'
    success_url = reverse_lazy('storage:obekt_list')

class listOrderMaterial(ListView):
    model = OrderMat
    fields = ['material', 'obekt', 'personal', ]
    template_name = 'storage/order_material_list.html'
    success_url = reverse_lazy('storage:order_material_list')
    def get_queryset(self):
            queryset = self.model.objects.filter(complete=True).order_by("date")

            return queryset


class createOrderMaterial(View):
    model = OrderMaterial
    fields = ['material', 'amount', 'obekt']
    template = 'storage/order_material_form.html'
    success_url = reverse_lazy('storage:material_type_list')
    def get(self, request):
        order_mat_form = OrderMaterialForm()
        order_form = OrderMatForm()
        mc = self.model.objects.all()

        ctx = {'order_mat_form': order_mat_form,'order_form': order_form}
        return render(request, self.template, ctx)

    def post(self, request):

        order_mat_form = OrderMaterialForm(request.POST)
        order_form = OrderMatForm(request.POST)
        if not order_form.is_valid():
            ctx = {'order_mat_form': order_mat_form,'order_form': order_form}
            return render(request, self.template, ctx)


        personal = request.user.personal
        obekt = personal.obekt

        order = order_form.save()
        order.personal = personal
        order.obekt = obekt


        values = {}
        for item in order_mat_form:
            for mat in request.POST.getlist(item.name):
                try:
                    values[item.name].append(mat)
                except:
                    values[item.name] = [mat]
        print(values)
        for idx,mat in enumerate(values['material']):
            if mat not in [None,'']:
                mat_obj = Material.objects.get(pk=int(values['material'][idx]))
                amount = int(values['amount'][idx])
                order.ordermaterial_set.create(material=mat_obj, amount=amount)


        order.save()

        return redirect(self.success_url)

class detailOrderMaterial(DetailView):
    model = OrderMat
    fields = ['material', 'obekt', 'personal', ]
    template_name = 'storage/order_material_detail.html'
    success_url = reverse_lazy('storage:material_type_list')
    def get(self, request, pk):
        if request.user.personal.position == 'Tc':

            ordermat = self.model.objects.get(pk=pk)
            if ordermat.personal == request.user.personal:
                ## render the view for the Technical that has created the order.
                ## This will be seen only once the order is approved by admin.
                ## The technical will confirm the amount of materials that they've received.
                ordermat = self.model.objects.get(pk=pk)
                proposed_material_per_obekt = {}
                obekti = []
                bases = Obekti.objects.filter(base=True)
                base_list = {}
                if bases.exists():
                    for base in bases:
                        base_list[base.id] = base
                for idx,ordermaterial in enumerate(ordermat.ordermaterial_set.all()):
                    materials_proposed = ordermaterial.ordermaterialperobekt_set.all()

                    material_in_obekt = []
                    for m in materials_proposed:
                        if m.obekt not in bases:
                            try:
                                material_in_obekt.append([MaterialPerObekt.objects.get(obekt=m.obekt, material=m.order_material.material).amount,m.amount,{'id':m.id,'allowed':m.allowed}])
                            except:
                                material_in_obekt.append([0,m.amount,{'id':m.id,'allowed':m.allowed}])
                            if m.obekt not in obekti:
                                obekti.append(m.obekt)
                    proposed_material_per_obekt[ordermaterial.id] = {
                        'obekts': material_in_obekt,
                        'materials_proposed': materials_proposed,
                    }

                obekts = proposed_material_per_obekt[ordermat.ordermaterial_set.first().id]['materials_proposed']
                form = OrderMatPerObektForm()
                form_transport = OrderMatFormTransport()
                if ordermat.transport != None:
                    form_transport = OrderMatFormTransport(initial={'transport': ordermat.transport})

                bases = Obekti.objects.filter(base=True)
                base_list = {}
                if bases.exists():
                    for base in bases:
                        base_list[base.id] = base

                ctx = {'ordermat': ordermat,
                    'proposed_material_per_obekt': proposed_material_per_obekt,
                    'form':form,
                    'obekts': obekti,
                    'position': request.user.personal.position,
                    'OrderMatFormTransport': form_transport,
                    'base_list': base_list,
                    'flag_tc_approve': 1,
                }
                #print(proposed_material_per_obekt.items())

                return render(request, self.template_name, ctx)

            else:
                ## render the view for Technicals from other obekts
                obekt = request.user.personal.obekt
                material_per_obekt = { i.material.id : i.amount for i in MaterialPerObekt.objects.filter(obekt=obekt) }
                order_mat_dict = {}
                materials_provided = {}
                for idx,ordermaterial in enumerate(ordermat.ordermaterial_set.all()):
                    materials_provided[ordermaterial] = ordermaterial.ordermaterialperobekt_set.filter(obekt=obekt)


                for mat in ordermat.ordermaterial_set.all():
                    if materials_provided[mat].exists():
                        try:
                            order_mat_dict[mat] = {
                                'amount_on_obekt': material_per_obekt[mat.material.id],
                                'materials_provided': materials_provided[mat],
                                'amount_provided': [i.amount for i in materials_provided[mat] if i.order_material.material.id == mat.material.id][0] if len([i.amount for i in materials_provided[mat] if i.order_material.material.id == mat.material.id]) else ''
                            }
                        except KeyError:
                            order_mat_dict[mat] = {
                                'amount_on_obekt': 'Няма налично',
                            }
                    else:
                        try:
                            order_mat_dict[mat] = {
                                'amount_on_obekt': material_per_obekt[mat.material.id],
                            }
                        except KeyError:
                            order_mat_dict[mat] = {
                                'amount_on_obekt': 'Няма налично',
                            }


                form = OrderMatPerObektForm()


                ctx = {'order_mat_dict': order_mat_dict,
                    'ordermat': ordermat,
                    'form':form,
                    'position': request.user.personal.position,
                }

                return render(request, self.template_name, ctx)


        elif request.user.personal.position == 'Ad':
            ordermat = self.model.objects.get(pk=pk)
            proposed_material_per_obekt = {}
            obekti = []
            bases = Obekti.objects.filter(base=True)
            base_list = {}
            if bases.exists():
                for base in bases:
                    base_list[base.id] = base
            for idx,ordermaterial in enumerate(ordermat.ordermaterial_set.all()):
                materials_proposed = ordermaterial.ordermaterialperobekt_set.all()

                material_in_obekt = []
                for m in materials_proposed:
                    if m.obekt not in bases:
                        try:
                            material_in_obekt.append([MaterialPerObekt.objects.get(obekt=m.obekt, material=m.order_material.material).amount,m.amount,{'id':m.id,'allowed':m.allowed}])
                        except:
                            material_in_obekt.append([0,m.amount,{'id':m.id,'allowed':m.allowed}])
                        if m.obekt not in obekti:
                            obekti.append(m.obekt)
                proposed_material_per_obekt[ordermaterial.id] = {
                    'obekts': material_in_obekt,
                    'materials_proposed': materials_proposed,
                }

            obekts = proposed_material_per_obekt[ordermat.ordermaterial_set.first().id]['materials_proposed']
            form = OrderMatPerObektForm()
            form_transport = OrderMatFormTransport()
            if ordermat.transport != None:
                form_transport = OrderMatFormTransport(initial={'transport': ordermat.transport})

            bases = Obekti.objects.filter(base=True)
            base_list = {}
            if bases.exists():
                for base in bases:
                    base_list[base.id] = base

            ctx = {'ordermat': ordermat,
                'proposed_material_per_obekt': proposed_material_per_obekt,
                'form':form,
                'obekts': obekti,
                'position': request.user.personal.position,
                'OrderMatFormTransport': form_transport,
                'base_list': base_list
            }
            #print(proposed_material_per_obekt.items())

            return render(request, self.template_name, ctx)


        elif request.user.personal.position == 'De':
            ordermat = self.model.objects.get(pk=pk)
            proposed_material_per_obekt = {}

            for idx,ordermaterial in enumerate(ordermat.ordermaterial_set.all()):
                materials_proposed = ordermaterial.ordermaterialperobekt_set.all()


                material_in_obekt = []
                for m in materials_proposed:
                    try:
                        material_in_obekt.append([MaterialPerObekt.objects.get(obekt=m.obekt, material=m.order_material.material).amount,m.amount,{'id':m.id,'allowed':m.allowed}])
                    except:
                        material_in_obekt.append([0,m.amount,{'id':m.id,'allowed':m.allowed}])

                proposed_material_per_obekt[ordermaterial.id] = {
                    'obekts': material_in_obekt,
                    'materials_proposed': materials_proposed,
                }
            obekts = proposed_material_per_obekt[ordermat.ordermaterial_set.first().id]['materials_proposed']
            form = OrderMatPerObektForm()
            form_transport = OrderMatFormTransport()
            if ordermat.transport != None:
                form_transport = OrderMatFormTransport(initial={'transport': ordermat.transport})
            ctx = {'ordermat': ordermat,
                'proposed_material_per_obekt': proposed_material_per_obekt,
                'form':form,
                'obekts': obekts,
                'position': request.user.personal.position,
                'OrderMatFormTransport': form_transport,
            }
            #print(proposed_material_per_obekt.items())

            return render(request, self.template_name, ctx)



class detailOrderMaterialCompleted(DetailView):
    model = OrderMat
    fields = ['material', 'obekt', 'personal', ]
    template_name = 'storage/order_material_completed_detail.html'
    success_url = reverse_lazy('storage:material_type_list')
    def get(self, request, pk):
        if request.user.personal.position == 'Ad':
            ordermat = self.model.objects.get(pk=pk)
            proposed_material_per_obekt = {}
            obekti = []
            bases = Obekti.objects.filter(base=True)
            base_list = {}
            if bases.exists():
                for base in bases:
                    base_list[base.id] = base
            for idx,ordermaterial in enumerate(ordermat.ordermaterial_set.all()):
                materials_proposed = ordermaterial.ordermaterialperobekt_set.all()

                material_in_obekt = []
                for m in materials_proposed:
                    if m.obekt not in bases:
                        try:
                            material_in_obekt.append([MaterialPerObekt.objects.get(obekt=m.obekt, material=m.order_material.material).amount,m.amount,{'id':m.id,'allowed':m.allowed}])
                        except:
                            material_in_obekt.append([0,m.amount,{'id':m.id,'allowed':m.allowed}])
                        if m.obekt not in obekti:
                            obekti.append(m.obekt)
                proposed_material_per_obekt[ordermaterial.id] = {
                    'obekts': material_in_obekt,
                    'materials_proposed': materials_proposed,
                }

            obekts = proposed_material_per_obekt[ordermat.ordermaterial_set.first().id]['materials_proposed']
            form = OrderMatPerObektForm()
            form_transport = OrderMatFormTransport()
            if ordermat.transport != None:
                form_transport = OrderMatFormTransport(initial={'transport': ordermat.transport})

            bases = Obekti.objects.filter(base=True)
            base_list = {}
            if bases.exists():
                for base in bases:
                    base_list[base.id] = base

            ctx = {'ordermat': ordermat,
                'proposed_material_per_obekt': proposed_material_per_obekt,
                'form':form,
                'obekts': obekti,
                'position': request.user.personal.position,
                'OrderMatFormTransport': form_transport,
                'base_list': base_list
            }
            #print(proposed_material_per_obekt.items())

            return render(request, self.template_name, ctx)



    def post(self, request,pk):
        if request.user.personal.position == 'Tc':
            ordermat = self.model.objects.get(pk=pk)

            if ordermat.personal == request.user.personal:
                for idx,ordermaterial in enumerate(ordermat.ordermaterial_set.all()):
                    for mat in ordermaterial.ordermaterialperobekt_set.all():
                        try:
                            mat.allowed = request.POST.get("allowed-{}".format(mat.id))
                            mat.save()
                        except:
                            pass

                ordermat.complete = True
                for idx,ordermaterial in enumerate(ordermat.ordermaterial_set.all()):
                    for mat_per_obekt in ordermaterial.ordermaterialperobekt_set.all():
                        for mat_in_obekt in mat_per_obekt.obekt.materialperobekt_set.all():
                            if mat_in_obekt.material.id == ordermaterial.material.id:
                                mat_in_obekt.amount = mat_in_obekt.amount - mat_per_obekt.allowed
                                mat_in_obekt.save()
                                obekt_save_to = ordermat.obekt.materialperobekt_set.filter(material__id=ordermaterial.material.id)
                                if obekt_save_to.exists():
                                    obekt_save_to = obekt_save_to[0]
                                    obekt_save_to.amount = obekt_save_to.amount + mat_per_obekt.allowed
                                    obekt_save_to.save()
                                else:
                                    ordermat.obekt.materialperobekt_set.create(material=ordermaterial.material, amount=mat_per_obekt.allowed)
                ordermat.save()
            else:
                amount_allowed = request.POST.getlist("amount")
                obekt = request.user.personal.obekt
                for idx,ordermaterial in enumerate(ordermat.ordermaterial_set.all()):
                    ordermaterial.ordermaterialperobekt_set.update_or_create(obekt=obekt, defaults={'amount': amount_allowed[idx]})

        elif request.user.personal.position == 'Ad':
            ordermat = self.model.objects.get(pk=pk)
            form_transport = OrderMatFormTransport(request.POST)
            if form_transport.is_valid():
                ordermat.transport = form_transport.cleaned_data['transport']
                ordermat.approved = True
                ordermat.save()

            for idx,ordermaterial in enumerate(ordermat.ordermaterial_set.all()):
                for mat in ordermaterial.ordermaterialperobekt_set.all():
                    try:
                        mat.allowed = request.POST.get("allowed-{}".format(mat.id))
                        mat.save()
                    except:
                        pass

            bases = Obekti.objects.filter(base=True)
            for idx,ordermaterial in enumerate(ordermat.ordermaterial_set.all()):
                for base in bases:
                    allowed = request.POST.get("base-allowed-{}-{}".format(base.id, ordermaterial.material.id))
                    if allowed not in [None, '', 0, 0.0]:
                        ordermaterial.ordermaterialperobekt_set.update_or_create(obekt=base, defaults={'allowed': allowed})



        return redirect(self.success_url)


class updateOrderMaterial(UpdateView):
    model = OrderMaterial
    fields = ['material', 'amount', 'obekt']
    template = 'storage/order_material_form.html'
    success_url = reverse_lazy('storage:material_type_list')
    def get(self, request, pk):
        order_mat_form = OrderMaterialForm()
        mc = self.model.objects.all()
        ordermat = OrderMat.objects.get(pk=pk)
        order_form = OrderMatForm(initial={'date': ordermat.date})
        ordermat_array = [[i.material.id, float(i.amount)] for i in ordermat.ordermaterial_set.all()]
        order_mat_completed_form = {}
        if ordermat.approved:
            order_mat_completed_form = OrderMatFormCompleted()
        ctx = {'order_mat_form': order_mat_form,
            'order_form': order_form,
            'ordermat': ordermat,
            'ordermat_array': ordermat_array,
            'order_mat_completed_form':order_mat_completed_form,
        }
        return render(request, self.template, ctx)

    def post(self, request, pk):
        ordermat = OrderMat.objects.get(pk=pk)
        order_mat_form = OrderMaterialForm(request.POST)
        order_form = OrderMatForm(request.POST)
        if not order_form.is_valid():
            ctx = {'order_mat_form': order_mat_form,'order_form': order_form}
            return render(request, self.template, ctx)




        values = {}
        for item in order_mat_form:
            for mat in request.POST.getlist(item.name):
                try:
                    values[item.name].append(mat)
                except:
                    values[item.name] = [mat]
        for idx,ordermaterial in enumerate(ordermat.ordermaterial_set.all()):
            mat_obj = Material.objects.get(pk=int(values['material'][idx]))
            amount = int(values['amount'][idx])
            ordermaterial.material = mat_obj
            ordermaterial.amount = amount
            ordermaterial.save()

        return redirect(self.success_url)

class deleteOrderMaterial(DeleteView):
    model = OrderMat
    template_name = 'storage/order_material_delete.html'
    success_url = reverse_lazy('storage:order_material_list')




class createOrderMachine(View):
    model = OrderMachine
    fields = ['machine', 'hours', 'obekt', 'date']
    template = 'storage/order_machine_form.html'
    success_url = reverse_lazy('storage:machine_list')
    def get(self, request):
        form = OrderMachineForm()
        mc = self.model.objects.all()

        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request):
        form = OrderMachineForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)
        hour = form.cleaned_data['hours']
        hour_check = []
        hour_check.append(hour)
        if hour in [1,2]:
            hour_check.append(3)

        machine = form.cleaned_data['machine']
        date = form.cleaned_data['date']
        for h in hour_check:
            ordermachine = self.model.objects.filter(machine=machine, date=date, hours=h)
            if ordermachine.exists():
                ctx = {'form': form, 'error': 'Машината е запазена за този час/ден.'}
                return render(request, self.template, ctx)
        personal = request.user.personal
        order = form.save()
        order.personal = personal
        order.save()

        return redirect(self.success_url)



class listOrderMachine(ListView):
    model = OrderMachine
    fields = ['machine', 'hours', 'obekt', 'date']
    template_name = 'storage/order_machine_list.html'


class detailOrderMachine(DetailView):
    model = OrderMachine
    fields = ['machine', 'hours', 'obekt', 'date']
    template_name = 'storage/order_machine_detail.html'
    def get(self, request, pk):
        ordermachine = self.model.objects.get(pk=pk)
        hours_scheduled = {'1': '8:00 - 12:00',
        '2': '13:00 - 17:00',
        '3': '8:00 - 17:00' }

        ctx = {'ordermachine': ordermachine, "hours_scheduled": hours_scheduled[ordermachine.hours]}
        return render(request, self.template_name, ctx)