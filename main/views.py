import os
from django.shortcuts import render, redirect, get_object_or_404
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.files.base import File
from django.http import FileResponse
from .models import Input, Output


def start():
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    if not os.path.exists("inputs"):
        os.makedirs("inputs")
    # Importing new employees in bulk
    processfiles_scheduler = BackgroundScheduler()
    print("cron job in progress...")
    processfiles_scheduler.add_job(process_files, "interval", seconds=10, coalesce=True)
    processfiles_scheduler.start()


def convert(input_instance):
    try:
        input_instance.status = "1"
        input_instance.save()
        with open(input_instance.file.path, "r", encoding="ISO-8859-1") as i:
            line = i.read()
        print("S1")
        length = len(line)
        print("S2")
        iteration_limit = 1000
        print("S3")
        iteration_counter = 0
        output_file = "outputs/{}-output.txt".format(
            input_instance.file.name.split("/")[-1]
        )

        with open(output_file, "w") as o:
            print("S4")
            x = 0
            y = 300
            print("S5")
            while True:
                o.writelines(line[x:y])
                if y != length:
                    o.writelines("\n")
                    x += 300
                    y += 300
                else:
                    break
        Output.objects.create(
            input_fk=input_instance, file=File(open(output_file, "rb"))
        )
        input_instance.status = "2"
        input_instance.save()
        print(
            "############################################################################### S13"
        )
    except Exception as e:
        print("S14")
        print("The bitch file attribute has no file associated with it.", e)
        return -1

    return 1


def process_files():
    inputs = Input.objects.exclude(status="2")
    for i in inputs:
        print(f"found input file: {i}")
        convert(i)


def download_output(request, pk):
    output = get_object_or_404(Output, id=pk)
    response = FileResponse(open(output.file.path, "rb"))
    response["Content-Disposition"] = 'attachment; filename="{}"'.format(
        output.file.name.split("/")[-1]
    )
    return response


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
                o_id = output.id
                otimestamp = output.file
            else:
                output = ""
                ofile = "N/A"
                o_id = "0"
                otimestamp = "N/A"
            inputs_data.append(
                {
                    "input_file": input_instance.file,
                    "input_timestamp": input_instance.timestamp,
                    "input_status": input_instance.status,
                    "output_file": ofile,
                    "output_id": o_id,
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
