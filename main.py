"""
**********************************************************************************************************************
Student ID              :   22141506
University              :   Birmingham City University
Course                  :   Msc Artificial Intelligence
Module Title            :   Computing for Artifiicail Intelligence
Module Code             :   CMP6221
Assessment Title        :   Portfolio of Secured database-enabled programs 
Assessment Type         :   CWRK
School                  :   School of Computing and Digital Technology
Module Co-ordinator     :   Salameh Abu Rmeileh
Code Created Date       :   21-OCT-2022
DataBase                :   MongoDB (ATLAS)
GUI                     :   TKinter V8.6
Programmming Language   :   Python V3.9.12
Assessment Summary      :
        This is an individual assessment that requires you to submit a portfolio of secure database-enabled programs 
to meet the labs and the case study brief. Your portfolio should include all the labs solutions and your solution 
to the case study as Python programs.

Program Description     : 
        The Car Evaluation DataSet which acts as a source file was downloaded from the Kaggle sites as a 
CSV file format. Then it is uploaded into the mongoDB Atlas Cloud platform which act as a reliable cloud Database
to store, retrieve and process the Data efficiently.
After Stored the data has been retrived and cleaned with the help of the Pandas library to make the data suitable 
for training and testing to make prediction using Decision Tree Algorithm (Gini Impurities)
The Program GUI(Graphical User Interface) was implemented using Tkinter.

Steps To be followed:
    1. Login to the Application using valid Authendication
        DataBase Login Details  :
                 UserName       : <admin>
                 Password       : <pass>
    2. Process the Data:
            (I)  Load the Data
            (II) View Data
    3. Go back and select the DECISION TREE button

    4. Process the Algorithm
            
    5. See the Output 

Code History            :
**********************************************************************************************************************
*   VERSIONS   *     MODIFIED DATE     *     DESCRIPTIONS                                                            *
**********************************************************************************************************************
*              *                       *                                                                             *
*    1.O       *     21-OCT-2022       *    Code Crearted                                                            *     
*              *                       *                                                                             *
**********************************************************************************************************************
*              *                       *                                                                             *
**********************************************************************************************************************


"""
# importing the library

from    tkinter                 import *
import  tkinter                 as     tk
from    tkinter                 import ttk
from    pymongo                 import *
from    sklearn.model_selection import train_test_split
from    sklearn.tree            import DecisionTreeClassifier
import  pandas                  as     pd
import  matplotlib              as     plt
import  csv
import  category_encoders       as     ce
from    sklearn.metrics         import accuracy_score, classification_report
from    sklearn.tree            import DecisionTreeClassifier
import  scikitplot.metrics      as     skplt
from    sklearn                 import tree
from    sklearn.model_selection import GridSearchCV
from    PIL                     import Image,ImageTk


LARGE_FONT= ("Verdana", 12)

# Declaring and connecting the mongoDB using pymongo as global, so that it can be access by every class

# Connecting to the DataBase 
try:
    Connection = MongoClient("mongodb://<admin>:<pass>@ac-o3yo7vf-shard-00-00.bgi3n46.mongodb.net:27017,ac-o3yo7vf-shard-00-01.bgi3n46.mongodb.net:27017,ac-o3yo7vf-shard-00-02.bgi3n46.mongodb.net:27017/?ssl=true&replicaSet=atlas-1l97cy-shard-0&authSource=admin&retryWrites=true&w=majority")
except Exception:
    print("Connection to the Server is unsuccessful")

# DB -> DataBase & LDcollection -> Login Details Collection             
DB                = Connection['Secure_DB_Assignment']
LDcollection      = DB['Login_details']
CarDataCollection = DB['Car_details']

# HomeScreen Class is used to define the Frame for navigating the pages
class HomeScreen(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for F in (LoginPage, StartPage, DataAndLoad, DTree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    

# Defining the Class for Login page 
class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        LoignPageLabel  = tk.Label(self, text = "Login page", font = LARGE_FONT)
        LoignPageLabel.pack(pady = 10,padx = 10)

        #username label and text entry box
        usernameLabel = tk.Label(self, text="User Name")
        usernameLabel.pack()

        username      = tk.StringVar()
        usernameEntry = tk.Entry(self, textvariable = username, bg = "grey89")
        usernameEntry.pack()

        #password label and password entry box
        passwordLabel = tk.Label(self, text="Password")
        passwordLabel.pack()

        password      = tk.StringVar()
        passwordEntry = tk.Entry(self, textvariable = password, show = '*', bg = "grey89")
        passwordEntry.pack()
    
        LoginCheck      = False
        LoginPageButtom = tk.Button(self, text = "Login", 
                        command =lambda: self.validateLogin(controller, LoginCheck, username.get(), password.get(), 
                                LoginPageButtom, usernameEntry, passwordEntry))
        LoginPageButtom.pack()
        
         
    '''
    validateLogin function will validate the authendication and 
    if success it will navigate to Start page else it will show invalid login 
    '''
    def validateLogin(self, controller, LoginCheck, username, password, LoginPageButtom,usernameEntry, passwordEntry):
        usernameEntry.delete(0,100)
        passwordEntry.delete(0,100)

        myFindingQuery1 = LDcollection.find()
        for i in myFindingQuery1:    #  Authendication Check
            for j in i["Login_detail"]: 
                if (j['UserName'] == username and j['Password'] == password): 
                        LoginCheck = True
                        break

        Success         = tk.StringVar()
        if LoginCheck == True:
            Success.set("Login Success, Click Next Page to continue")
            Loginresult     = tk.Label(self, textvariable = Success)
            Loginresult.pack()
            LoginPageButtom.configure(text= "Next Page", command = lambda: controller.show_frame(StartPage))
            
        else:
            Success.set("User Name or Password is invalid")
            Loginresult     = tk.Label(self, textvariable = Success)
            Loginresult.pack()
            LoginPageButtom.configure(text= "Login")

    

# Class act as the starting page of the Interface once the Authendication is success     
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        label           = tk.Label(self, text="Home Screen", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        Databutton      = tk.Button(self, text="PROCESS DATA",
                            command=lambda: controller.show_frame(DataAndLoad))
        Databutton.pack()
        
        DTReebutton     = tk.Button(self, text="DECISION TREE",
                            command=lambda: controller.show_frame(DTree))
        DTReebutton.pack()
    

class DataAndLoad(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Data And Load Page!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        HomeButton          = tk.Button(self, text="Back to Home",
                              command=lambda: controller.show_frame(StartPage))
        HomeButton.pack()

        Loadbutton          = tk.Button(self, text="LOAD DATA",
                              command=lambda: self.LoadIntoMongoDB())
        Loadbutton.pack()
        
        #CarData  = pd.read_csv('car_evaluation.csv')
        ShowButtom           = tk.Button(self, text="VIEW DATA",
                               command=lambda: self.displayCSVdata())
        ShowButtom.pack(side = "top")
        
    # displaCSVdata -> Displaying the Uncleaned DATA              
    def displayCSVdata(self):

        # Creating a table view to show the Data
        TableMargin = Frame(self, width=500)
        TableMargin.pack(side = TOP)
        scrollbarx  = Scrollbar(TableMargin, orient=HORIZONTAL)
        scrollbary  = Scrollbar(TableMargin, orient=VERTICAL)
        tree        = ttk.Treeview(TableMargin, 
        columns     =("buying_price","maintenance_cost","number_of_doors","number_of_persons","lug_boot","safety","decision"), 
                    height=400, selectmode="extended", yscrollcommand=scrollbary.set, 
                    xscrollcommand=scrollbarx.set)

        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)

        #buying price,maintenance cost,number of doors,number of persons,
        # lug_boot,safety,decision
        tree.heading('buying_price',      text="buying price",      anchor=W)
        tree.heading('maintenance_cost',  text="maintenance cost",  anchor=W)
        tree.heading('number_of_doors',   text="number of doors",   anchor=W)
        tree.heading('number_of_persons', text="number of persons", anchor=W)
        tree.heading('lug_boot',          text="lug_boot",          anchor=W)
        tree.heading('safety',            text="safety",            anchor=W)
        tree.heading('decision',          text="decision",          anchor=W)

        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=200)
        tree.column('#2', stretch=NO, minwidth=0, width=200)
        tree.column('#3', stretch=NO, minwidth=0, width=300)
        tree.pack()

        # opening the CSV file to insert the data into the Tableview
        with open(r'car_evaluation.csv') as f:
            CarData = csv.DictReader(f, delimiter=',')
            for row in CarData:
                buying_price        = row['buying price']
                maintenance_cost    = row['maintenance cost']
                number_of_doors     = row['number of doors']
                number_of_persons   = row['number of persons']
                lug_boot            = row['lug_boot']
                safety              = row['safety']
                decision            = row['decision']

                tree.insert("", 0, values=(buying_price, maintenance_cost, number_of_doors,
                 number_of_persons, lug_boot, safety, decision))

    # LoadIntoMongoDB -> Loading the Cleaned DATA into the MongoDB(ATlas)
    def LoadIntoMongoDB(self):

        col_list = DB.list_collection_names()

        for i in col_list:          # dropping the Collection if its already exist in order to avoid overriding the data or mismatch
            if i == 'Car_details':
                CarDataCollection.drop()      
            
        ''' # snippet to convert CSV to json  --- Testin Purpose
        PD_CarDAta  = pd.read_csv("car_evaluation.csv")
        PD_CarDAta.to_json("car_evaluation_json.json")
        CarDAtaCreateJson = open("car_evaluation_json.json")
        CarDataJson       = json.load(CarDAtaCreateJson)
        '''
        
        PD_CarDAta      =  pd.read_csv(r"car_evaluation.csv")
        CarDataDict     =  PD_CarDAta.to_dict(orient="records")
        CarDataCollection.insert_many(CarDataDict)
        
        CarDataFrame    =    pd.DataFrame(CarDataCollection.find())
        
        # To Check whether Data is successfully inserted or not
        if CarDataFrame.empty  == True:
            DataLoadedlabel    = tk.Label(self, text="Data is not Inserted ", font=LARGE_FONT)
            DataLoadedlabel.pack(pady=10,padx=10)
        else:
            DataLoadedlabel    = tk.Label(self, text="All Data are Loaded ", font=LARGE_FONT)
            DataLoadedlabel.pack(pady=10,padx=10)


class DTree(tk.Frame):  

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Decision Tree", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        HomeButton      = tk.Button(self, text="Back to Home",
                          command =lambda: controller.show_frame(StartPage))
        HomeButton.pack()

        AlgorithmButtom = tk.Button(self, text= "Process DecisionTree Algorithm", 
                          command =lambda: self.Algorithm(AlgorithmButtom))
        AlgorithmButtom.pack()
        
        
    def Algorithm(self, AlgorithmButtom):    
        CarDataFrame    =    pd.DataFrame(CarDataCollection.find())
       #CarDataFrame    = CarDataFrame.drop(columns = '_id', axis = 1) #Dropping the _id Column 

        # Checking the Details of the CarDataFrame DataFrame
        print(CarDataFrame.head(5))
        print(CarDataFrame.info())
        print(CarDataFrame.isnull().sum())

        try:
        # Training, Testing and Cross Validating the Data Set    
            X = CarDataFrame.drop(['_id', 'decision'], axis = 1) # Dropping the Targeted column 
            Y = CarDataFrame['decision']                        # Setting  the Targeted Column 
        except KeyError:
            print("Not a problem")

        print(X.shape, Y.shape)

        """
         encoding will automatically convert the string values into the integer format
         category_encoders help us to encode the data automatically according to the value
         Eg:
            Low  -> 1
            Mid  -> 2
            High -> 3
        """     
        encoding = ce.OrdinalEncoder(cols=["buying price", "maintenance cost", "number of doors", "number of persons", "lug_boot", "safety"])
        x        = encoding.fit_transform(X)

        '''
         Train Test Split:
            For Testing the Data Set : 30%
            For Traning the Data Set : 30%

            CV - > Cross Validation
        '''        

        x1, xtest, y1, ytest        = train_test_split(x,  Y,  test_size=0.3, random_state=2)
        xtrain, x_CV, ytrain, y_CV  = train_test_split(x1, y1, test_size=0.3, random_state=2)

        # Exploring class distribution under train ,crossvalidation and test dataset
        print('\n Training Dataset',xtrain.shape,ytrain.shape)
        print('\n Class label distribution in Training Set\n',ytrain.value_counts())
        print('\n ***********')
        print("\n CrossValidation Dataset",x_CV.shape,y_CV.shape)
        print('\n Class label distribution in Cross Validation Set\n',y_CV.value_counts())
        print('\n ***********')
        print("\n Test Dataset",xtest.shape,ytest.shape)
        print('\n Class label distribution in Test Set\n',ytest.value_counts())

        # Grid Search
        parameters={'max_depth': list(range(1,30)),
            'min_samples_leaf' : list(range(5,200,20)),
            'min_samples_split': list(range(5,200,20))
            }
        model = GridSearchCV(DecisionTreeClassifier(class_weight='balanced'),parameters,n_jobs=-1,cv=10,scoring='accuracy')
        model.fit(xtrain,ytrain)
        print(model.best_estimator_)
        print("\n",model.best_params_)
        print("\n",model.score(x_CV,y_CV))

        
        ypredict = model.predict(x_CV)
        accuracy = accuracy_score(y_CV,ypredict,normalize=True)*float(100)
        print('\n\n classification report')
        print(classification_report(y_CV,ypredict))
        skplt.plot_confusion_matrix(y_CV,ypredict)

        clf = tree.DecisionTreeClassifier(class_weight='balanced',max_depth=9,min_samples_leaf=5,min_samples_split=5)
        clf.fit(xtrain,ytrain)
        ypredict = clf.predict(xtest)
        accuracy = accuracy_score(ytest,ypredict,normalize=True)*float(100)
        print('\n Accuracy score is',accuracy)
        print('\n classification report')
        print(classification_report(ytest,ypredict))
        skplt.plot_confusion_matrix(ytest,ypredict)

        # Visualising Decision Tree
        cols = ["buying price", "maintenance cost", "number of doors", "number of persons", "lug_boot", "safety"]
        trgt = [' acc','good','unacc ',' vgood']
        
        # processing the Plot and saving it in a PNG formate (Filename : DecisionTreeOutput.png)
        fig, axes = plt.pyplot.subplots(nrows = 1,ncols = 1,figsize = (4,4), dpi=500)
        tree.plot_tree(clf,
                    feature_names =cols, 
                    class_names=trgt,
                    filled = True);
        fig.savefig('DecisionTreeOutput.png')
        
        AlgorithmButtom.configure(text= "Processed")  

        # Button to show the output
        DTreeoutbutton  = tk.Button(self, text="OUTPUT",  
                            command=lambda: self.OutputDisplay())
        DTreeoutbutton.pack()

        ''' -- Testing purpose
        img= tk.PhotoImage(file = str("DecisionTreeOutput.png"))
        canvas = tk.Canvas(self, width = 1000, height = 1000)      
        canvas.pack() 
        canvas.create_image(800,800,anchor=NW,image=img)
        
        img= ImageTk.PhotoImage(Image.open("DecisionTreeOutput.png"))
        canvas = tk.Canvas(self, width = 800, height = 800)      
        canvas.pack() 
        canvas.create_image(700,700,anchor=NW,image=img)
        '''

    def OutputDisplay(self):    
             
       # Used Image lib to pull up the png file 
        img                  = (Image.open(str("DecisionTreeOutput.png")))
        img                  = img.resize((1000,800), Image.ANTIALIAS)
        new_image            = ImageTk.PhotoImage(img)
        ImgOutputLabel       = tk.Label(self, image=new_image)
        
        ImgOutputLabel.image = new_image
        ImgOutputLabel.pack()

        quitButton  = tk.Button(self, text="QUIT",  
                            command=lambda: app.destroy())
        quitButton.pack()

        ''' -- Testing
        canvas = tk.Canvas(self, width = 1000, height = 1000)      
        canvas.pack() 
        canvas.create_image(800,800,anchor=NW,image=img)
        '''       

app = HomeScreen()
app.geometry('1500x1500')
app.title("Decision Tree")
app.mainloop()

#************************************ End of the Program ****************************************************************