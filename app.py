from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

YOGA_PATH = app.root_path + '/classes.csv'

YOGA_KEYS = ['name','type','level','date','duration','trainer','description']       #keys for yoga class data


def get_yogas():                                                                    #
    with open(YOGA_PATH, 'r', encoding='utf-8') as csvfile:
            data = csv.DictReader(csvfile)
            yoga_classes = {}
            for yoga in data:
                yoga_classes[yoga['name']] = yoga
                
    return yoga_classes


def set_yogas(yoga_classes):
    with open(YOGA_PATH, mode ='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=YOGA_KEYS)
        writer.writeheader()
        for yoga in yoga_classes.values():
            writer.writerow(yoga)
            

            
        
            
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classes')
def classes():
    yoga_classes = get_yogas()
    return render_template('classes.html', yoga_classes = yoga_classes)



@app.route('/classes/<class_id>')
def class_detail(class_id=None):
    yoga_classes = get_yogas()
    if class_id and class_id in yoga_classes.keys():
        yoga_class = yoga_classes[class_id]
        return render_template('class.html', class_id=class_id, yoga_class=yoga_class)
    else:
        return render_template('classes.html', yoga_classes=yoga_classes)


    



@app.route('/classes/create', methods=['GET', 'POST'])
def create(class_id=None):
    
   if request.method == 'POST':
       
       yoga_classes = get_yogas()
       
       newYoga={}
       
       newYoga['name'] = request.form['name']
       newYoga['type'] = request.form['type']
       newYoga['level'] = request.form['level']
       newYoga['date'] = request.form['date']
       newYoga['duration'] = request.form['duration']
       newYoga['trainer'] = request.form['trainer']
       newYoga['description'] = request.form['description']
       
       yoga_classes[request.form['name']] = newYoga
       
       set_yogas(yoga_classes)
      
       return redirect(url_for('classes'))
   
   else:
       return render_template('class_form.html')


@app.route('/classes/<class_id>/edit', methods=['GET', 'POST'])
def edit(class_id = None):
    yoga_classes = get_yogas()

    if request.method == 'POST':       
       newYoga={}      
       newYoga['name'] = request.form['name']
       newYoga['type'] = request.form['type']
       newYoga['level'] = request.form['level']
       newYoga['date'] = request.form['date']
       newYoga['duration'] = request.form['duration']
       newYoga['trainer'] = request.form['trainer']
       newYoga['description'] = request.form['description']
       
       
       yoga_classes[request.form['name']] = newYoga
       set_yogas(yoga_classes)
      
       return redirect(url_for('classes', class_id = class_id))
   
    else:
       yoga_classes=get_yogas()
       new_yoga=yoga_classes[class_id]
       return render_template('class_form.html', new_yoga=new_yoga, yoga_classes=yoga_classes)
   
   
@app.route('/classes/<class_id>/delete')
def delete(class_id=None):
    yoga_classes = get_yogas()
    if class_id and class_id in yoga_classes.keys():
        yoga_class = yoga_classes[class_id]
        return render_template('delete_form.html', class_id=class_id, yoga_class=yoga_class)

@app.route('/classes/<class_id>/delete/delete_confirm')
def delete_confirm( class_id=None):
    yoga_classes=get_yogas()
    if class_id and class_id in yoga_classes.keys():
        yoga_class = yoga_classes[class_id]
        yoga_class['name'] = ""
        yoga_class['type'] = ""
        yoga_class['level'] = ""
        yoga_class['date'] = ""
        yoga_class['duration'] = ""
        yoga_class['trainer'] = ""
        yoga_class['description'] = ""
            
        yoga_classes[class_id] = yoga_class
        set_yogas(yoga_classes)
                    
        return render_template('delete_confirm.html')