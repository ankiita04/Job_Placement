import pickle
import json
import config
import numpy as np
from werkzeug.datastructures import MultiDict
import pymongo
import warnings
warnings.filterwarnings('ignore')


class JobPlacement():

    def __init__(self, gender,ssc_percentage, ssc_board,hsc_percentage,hsc_board,degree_percentage, work_experience,emp_test_percentage, specialisation,mba_percent,hsc_subject,undergrad_degree) :
        self.gender = gender
        self.ssc_percentage= ssc_percentage
        self.ssc_board = ssc_board
        self.hsc_board = hsc_board
        self.hsc_percentage= hsc_percentage
        self.degree_percentage= degree_percentage
        self.work_experience = work_experience
        self.emp_test_percentage= emp_test_percentage
        self.mba_percent=mba_percent
        self.specialisation = specialisation
        self.undergrad_degree=undergrad_degree
        self.hsc_subject = hsc_subject 

    def __database_init(self):
        mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
        database_name = 'placement_predict_db'
        db = mongo_client[database_name]
        self.collection_user_input = db['user_input']



    def __load_model(self): # Private Method
        # Load Model File
        with open(r'artifacts/regression_model.pkl', 'rb') as f:
            self.model = pickle.load(f)

        # Load Project Data 
        with open(r'artifacts/project_data.json','r') as f:
            self.project_data = json.load( f)



    def get_predict_placement(self): # Public Method
        self.__load_model()
        test_array = np.zeros((1,self.model.n_features_in_))
        test_array[0][1] = self.project_data['gender'][self.gender]
        test_array[0][2] = self.ssc_percentage
        test_array[0][3] = self.project_data["ssc_board"][self.ssc_board]
        test_array[0][4] = self.hsc_percentage
        test_array[0][5] = self.project_data["hsc_board"][self.hsc_board]
        test_array[0][6] = self.degree_percentage
        test_array[0][7] = self.project_data["work_experience"][self.work_experience]
        test_array[0][8] = self.emp_test_percentage
        test_array[0][9] = self.project_data["specialisation"][self.specialisation]
        test_array[0][10] = self.mba_percent
        undergrad_degree = 'undergrad_degree_' + self.undergrad_degree
        index = self.project_data['Column Names'].index(undergrad_degree)

        test_array[0][index] = 1
        hsc_subject = 'hsc_subject_' + self.hsc_subject
        index = self.project_data['Column Names'].index(hsc_subject)
        test_array[0][index] = 1


        # print("Test Array is :",test_array)

        self.predict_placement = int(np.around(self.model.predict(test_array)[0],3))
        print("Predicted Placement :", self.predict_placement)

        return self.predict_placement

    def database(self):
        self.get_predict_placement()
        self.__database_init()
        self.collection_user_input.insert_one({
            "gender" :self.gender, "ssc_percentage": self.ssc_percentage, "ssc_board" : self.ssc_board,
            "hsc_board" : self.hsc_board,"hsc_percentage": self.hsc_percentage,"degree_percentage": self.degree_percentage,
            "work_experience":self.work_experience,"emp_test_percentage":self.emp_test_percentage,"mba_percent": self.mba_percent,
            "specialisation":self.specialisation, "undergrad_degree":self.undergrad_degree, "hsc_subject":self.hsc_subject, "predict_placement":self.predict_placement

        })

        

if __name__ == '__main__':

    cls = JobPlacement('M',67,'Central',70,'Central',70,'No',88,'Mkt&Fin',80,'Arts','Comm&Mgmt')
    prediction = cls.get_predict_placement()
    cls.database()
    print(prediction)
    
