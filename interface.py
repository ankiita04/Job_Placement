from flask import Flask, render_template, jsonify, request
import config
from utils import JobPlacement
from werkzeug.datastructures import MultiDict
import traceback
app = Flask(__name__)

@app.route('/')
def home():
    return render_template ("text.html")


@app.route('/predict_placement', methods = ["GET","POST"])
def predict_placement():
    try:
        if request.method == "POST":
            data = request.form.get

            # print("User Data is :",data)
            gender = data('gender')
            ssc_percentage = eval(data("ssc_percentage"))
            ssc_board = data('ssc_board')
            hsc_board = data('hsc_board')
            hsc_percentage = eval(data("hsc_percentage"))
            degree_percentage = eval(data("degree_percentage")) 
            work_experience = data('work_experience')
            emp_test_percentage=eval(data("emp_test_percentage"))
            mba_percent = eval(data("mba_percent"))
            specialisation = data('specialisation')
            hsc_subject = data("hsc_subject")
            undergrad_degree = data("undergrad_degree")

            job_place = JobPlacement(gender,ssc_percentage, ssc_board,hsc_percentage,hsc_board,degree_percentage, work_experience,emp_test_percentage, specialisation,mba_percent,hsc_subject,undergrad_degree)
            placement = job_place.get_predict_placement()

            if placement == 1:
                return  render_template("text.html",Result = "You will placed")
            elif placement == 0 :
                return  render_template("text.html",Result ="You will not placed")
             
        else:
            data = request.args.get

            # print("User Data is :",data)
            gender = data('gender')
            ssc_percentage = eval(data("ssc_percentage"))
            ssc_board = data('ssc_board')
            hsc_board = data('hsc_board')
            hsc_percentage = eval(data("hsc_percentage"))
            degree_percentage = eval(data("degree_percentage")) 
            work_experience = data('work_experience')
            emp_test_percentage=eval(data("emp_test_percentage"))
            mba_percent = eval(data("mba_percent"))
            specialisation = data('specialisation')
            hsc_subject = data("hsc_subject")
            undergrad_degree = data("undergrad_degree")
            

            job_place = JobPlacement(gender,ssc_percentage, ssc_board,hsc_percentage,hsc_board,degree_percentage, work_experience,emp_test_percentage, specialisation,mba_percent,hsc_subject,undergrad_degree)
            placement = job_place.get_predict_placement()

            if placement == 1:
                return  render_template("text.html",Result = "You will placed")
            elif placement == 0 :
                return  render_template("text.html" ,Result = "You will not placed")
    except:
        print(traceback.print_exc())
        return  jsonify({"Message" : "Unsuccessful"})           


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = config.PORT_NUMBER,debug=False)