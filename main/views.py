from django.shortcuts import render, redirect
from apscheduler.schedulers.background import BackgroundScheduler

from .models import Input, Output


def start():
    # Importing new employees in bulk
    processfiles_scheduler = BackgroundScheduler()
    print("starting processing...")
    processfiles_scheduler.add_job(process_files, "interval", minutes=3)
    processfiles_scheduler.start()


def convert(input_instance):
    try:
        with input_instance.file.open("r") as i:
            line = i.read()

        length = len(line)
        iteration_limit = 1000
        iteration_counter = 0
        print("creatingthe out put file")
        output = Output.objects.create(input_fk=input_instance)
        print(f"output {output.id} created!")
        with output.file.open("w") as o:
            x = 0
            y = 300

            while True:
                iteration_counter += 1
                if iteration_counter > iteration_limit:
                    return -1

                if y > length:
                    o.writelines(line[x:])
                    break

                o.writelines(line[x:y])
                o.writelines("\n")
                x += 300
                y += 300
    except Exception as e:
        print("The bitch file attribute has no file associated with it.", e)
        return -1

    return 1


def process_files():
    inputs = Input.objects.exclude(status="2")
    for i in inputs:
        rsp = convert(i)

        if rsp == 1:
            i.status = "2"
        else:
            i.status = "1"
        i.save()


def home(request):
    if request.method == "POST":
        file = request.FILES.get("file_kw")
        Input.objects.create(file=file)
        return redirect("homepage")

    inputs = Input.objects.all()
    inputs_data = []

    if inputs:
        for input_instance in inputs:
            if input_instance.status == "2":
                output = Output.objects.get(input_fk=input_instance)
                ofile = output.file
                otimestamp = output.file
            else:
                output = ""
                ofile = "N/A"
                otimestamp = "N/A"
            inputs_data.append(
                {
                    "input_file": input_instance.file,
                    "input_timestamp": input_instance.timestamp,
                    "input_status": input_instance.status,
                    "output_file": ofile,
                    "output_timestamp": otimestamp,
                }
            )

    return render(
        request,
        "main/index.html",
        {
            "inputs_data": inputs_data,
        },
    )
