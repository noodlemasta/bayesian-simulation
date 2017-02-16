import sys
import math

def main():
    #Read Input File
    inputFile = open(sys.argv[2])
    input_name = sys.argv[2]
    output_name = input_name.split('.')[0] + "_inference." + input_name.split('.')[1]
    #First line
    mystring = inputFile.readline()
    #processed first line
    mylist = mystring.split()
    mylist[0] = int(mylist[0])
    mylist[1] = int(mylist[1])

    #list of diseases, # of symptoms, and probability of having the disease
    disease = []

    #dictionaries of the symptoms and their probabilities if the disease is and isn't true
    #dictionaries are keyed by disease names
    symptoms = {}
    disease_true = {}
    disease_false = {}

    #list of all the patient test data
    patients = []

    #list of Question 1 dictionaries
    result1 = mylist[1]*[]
    #list of Question 2 dictionaries
    result2 = mylist[1]*[]
    #list of Question 3 dictionaries
    result3 = mylist[1]*[]

    #Read in the disease data
    for i in range(mylist[0]):
        #One iteration of the disease input
        disease.append(inputFile.readline().split())
        #Convert the number of symptoms and probability to int and float
        disease[i][1] = int(disease[i][1])
        disease[i][2] = float(disease[i][2])
        symptoms[disease[i][0]] = eval(inputFile.readline())
        disease_true[disease[i][0]] = eval(inputFile.readline())
        disease_false[disease[i][0]] = eval(inputFile.readline())

    #Read in the patient data
    for i in range(mylist[1]):
        patient_tests = []
        for j in range(mylist[0]):
            patient_tests.append(eval(inputFile.readline()))
        patients.append(patient_tests)

    inputFile.close()

    outputFile = open(output_name, 'w')
    #Iterate through ALL of the patients
    for k in range(mylist[1]):
        result1.append({})
        result2.append({})
        result3.append({})
        
        #Iterate through all of the diseases for ONE patient and run all the tests
        for i in range(mylist[0]):
            result1[k][disease[i][0]] = "%.4f" % Bayes_Rule(patients[k][i], disease_true[disease[i][0]], disease_false[disease[i][0]], disease[i][2],disease[i][1])
            result2[k][disease[i][0]] = Min_Max(patients[k][i], disease_true[disease[i][0]], disease_false[disease[i][0]], disease[i][2],disease[i][1])
            result3[k][disease[i][0]] = Find_Test(patients[k][i], disease_true[disease[i][0]], disease_false[disease[i][0]], symptoms[disease[i][0]], disease[i][2],disease[i][1], result1[k][disease[i][0]])

        #Output patient data
        outputFile.write("Patient-" + str(k+1) + ":\n")
        outputFile.write(str(result1[k]))
        outputFile.write('\n')
        outputFile.write(str(result2[k]))
        outputFile.write('\n')
        outputFile.write(str(result3[k]))
        outputFile.write('\n')

    outputFile.close()

#Compute the Bayes Rule probability for one disease
def Bayes_Rule(tests, dis_true_prob, dis_false_prob, disease_prob, symptom_len):
    #Probability given the disease is true
    bayes_pos = disease_prob
    #Probability given the disease is false
    bayes_neg = 1 - disease_prob
    for i in range(symptom_len):
        if tests[i] == 'T':
            bayes_pos *= dis_true_prob[i]
            bayes_neg *= dis_false_prob[i]
        elif tests[i] == 'F':
            bayes_pos *= (1 - dis_true_prob[i])
            bayes_neg *= (1 - dis_false_prob[i])
    return bayes_pos/(bayes_pos + bayes_neg)

#Reassign U's into T/F values
def Binary_Convert(num, bits):
    assign_list = []
    #If num is 0, assign 'F' to the number of bits we need
    if num == 0:
        assign_list = bits*['F']
    #Do binary conversion on num, but use 'T' and 'F' instead of '1' and '0' respectively
    else:
        while num > 0:
            if num % 2 == 0:
                assign_list.insert(0, 'F')
            elif num % 2 == 1:
                assign_list.insert(0, 'T')
            num = num/2
            num = math.floor(num)
        #If we are done converting but we aren't at our desired bit length, add leading 'F's
        if len(assign_list) < bits:
            while len(assign_list) < bits:
                assign_list.insert(0, 'F')
    return assign_list

#Find the minimum and maximum probabilities due to U values
def Min_Max(tests, dis_true_prob, dis_false_prob, disease_prob, symptom_len):
    #List of the indecies that contain U values in this testing instance
    indecies_of_U = []
    #Number of U's in this testing instance
    count_of_U = 0
    #Min and Max probabilities in this testing instance
    min_prob = 1.0
    max_prob = 0.0
    #List to hold 2^(count_of_U) new test values
    new_tests = []
    for i in range(symptom_len):
        if tests[i] == 'U':
            indecies_of_U.append(i)
            count_of_U += 1
    for i in range(2**count_of_U):
        new_tests.append(tests[:])
        #Use Binary Convert to come up with an assignment of U based on the current iteration
        assign_of_U = Binary_Convert(i, count_of_U)
        #Iterate through the different U values in this test and change their values
        for j in range(len(indecies_of_U)):
            new_tests[i][indecies_of_U[j]] = assign_of_U[j]
        temp_prob = "%.4f" % Bayes_Rule(new_tests[i], dis_true_prob, dis_false_prob, disease_prob, symptom_len)
        #Determine what the min and max probabilities are
        if float(temp_prob) > max_prob:
            max_prob = float(temp_prob)     #Bayes_Rule returns a string for formatting, so I need to convert temp_prob to a float
        if min_prob > float(temp_prob):
            min_prob = float(temp_prob)
    return ("%.4f" % min_prob, "%.4f" % max_prob)

def Find_Test(tests, dis_true_prob, dis_false_prob, symptoms, disease_prob, symptom_len, calc_dis_prob):
    #List to hold all the new assignments of values
    new_tests = []
    #max and min probabilities in this testing instance
    max_prob = 0.0
    min_prob = 1.0
    #List to hold the values of the symptom and what truth assignment yields the max/min values in this testing instance
    max_list = []
    min_list = []
    #Flag value to show whether we did find a new max or min
    max_list_edit = False
    min_list_edit = False
    #List of the indecies that held a U value in the original list
    indecies_of_U = []
    #Number of U values in one disease testing instance 
    count_of_U = 0
    #List to hold the final max/min result
    final_result = []

    for i in range(symptom_len):
        #If one symptom test is U, add it to the list of U indecies and make new tests with reassigned values for this U
        if tests[i] == 'U':
            indecies_of_U.append(i)
            count_of_U += 1
            #True assignment of U
            temp_true = tests[:]
            temp_true[i] = 'T'
            new_tests.append(temp_true)
            #False assignment of U
            temp_false = tests[:]
            temp_false[i] = 'F'
            new_tests.append(temp_false)
    if count_of_U > 0:
        for i in range(len(new_tests)):
            temp_prob = "%.4f" % Bayes_Rule(new_tests[i], dis_true_prob, dis_false_prob, disease_prob, symptom_len)  
            #Check if this new probability is larger than the result from Question 1 AND any previously tested probability from this part
            if float(temp_prob) > float(calc_dis_prob) and max_prob < float(temp_prob):
                max_prob = float(temp_prob)             #Bayes_Rule returns a string for formatting, so I need to convert temp_prob to a float
                if i%2 == 0:
                    max_list = [symptoms[indecies_of_U[i/2]], 'T']
                elif i%2 == 1:
                    max_list = [symptoms[indecies_of_U[(i-1)/2]], 'F']
                max_list_edit = True
            #Check if this new probability is smaller than the result from Question 1 AND any previously tested probability from this part
            if float(calc_dis_prob) > float(temp_prob) and min_prob > float(temp_prob):
                min_prob = float(temp_prob)
                if i%2 == 0:
                    min_list = [symptoms[indecies_of_U[i/2]], 'T']
                elif i%2 == 1:
                    min_list = [symptoms[indecies_of_U[(i-1)/2]], 'F']
                min_list_edit = True
            #If we haven't found any larger/smaller probability, then we output ['none', 'N']
            if not max_list_edit:
                max_list = ['none', 'N']
            if not min_list_edit:
                min_list = ['none', 'N']
        final_result = max_list[:] + min_list[:]
    #If we did not have any U values for the tests, then we output ['none', 'N'] for both the max and min change
    else:
        final_result = ['none', 'N', 'none', 'N']
    return final_result
    


main()
