import imp
import math
import numpy as np
from plot_errors import plot_list_error
from utils import *
from config_loader import expoint
from config_utils import parseNumbers
from perceptrons.MultilayerPerceptron import *
import random
from plot_errors import plot as plot_errors, plot_list_error
from plot_accuracies import plot_acc
from plot_predictions import plot_predictions

def ex3():
    np.random.seed(1)
    if expoint == 1:
        ex3_1()
    elif expoint == 2:
        ex3_2()
    elif expoint == 3:
        ex3_3()

def ex3_1():
    train_data = np.array([
        [-1, 1],
        [1, -1],
        [-1, -1],
        [1, 1]
    ])
    #train_data = np.array(list(map(lambda x: np.append(x,1), train_data)))
    xor_expected_data = np.array([[1], [1], [-1], [-1]])

    perceptron = MultiLayerPerceptron([
        NeuronLayer(3, inputs=train_data.shape[1], activation="linear"),
        NeuronLayer(5),
        NeuronLayer(xor_expected_data.shape[1])
    ])

    min_error, errors, ii, training_accuracies, test_accuracies, min_error_test = perceptron.train(train_data, xor_expected_data, train_data, xor_expected_data, 1, iterations_qty=10000)

    #plot(ii, [errors], ['errors'], 'Epoch', 'Errors', 'Mean Squared Error vs Epochs - multilayer')

    print('Error minimo: ', min_error)
    print('Error minimo test: ', min_error_test)
    plot_list_error(errors)
    plot_acc(ii,training_accuracies,test_accuracies)

def ex3_2():
    numbers = parseNumbers('./entries_3.txt')
    expected = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1]

    #Start Cross validations::
    k = 3
    first_layer_size = math.floor(((k-1) * len(numbers)) / k)

    splitsA = truncate(numbers, k)
    splitsE = truncate(expected, k)
    train_data = []
    expected_data = []

    for i in range(k):
        print('TEST ID: ', i)
        testID = i
        test_data = splitsA[testID]
        expected_test = splitsE[testID]

        train_data = []
        expected_data = []
        for j in range(k):
            if j != testID:
                for num in splitsA[j]:
                    train_data.append(num)
                for num in splitsE[j]:
                    expected_data.append(num)

        to_test = []
        lenn = math.floor(10 / k)
        for j in range(lenn):
            to_test.append((lenn * (testID)) + j)
        if testID == k - 1:
            to_test.append((lenn * (testID)) + lenn)
        to_train = []
        for j in range(10):
            if j not in to_test:
                to_train.append(j)

        train_data = np.array(train_data)
        expected_data = np.array(expected_data)

        # print("to train:", to_train)
        # print("train data:", train_data)
        # print("expected data:", expected_data)
        # print()

        test_data = np.array(test_data)
        expected_test = np.array(expected_test)

        perceptron = MultiLayerPerceptron([
            NeuronLayer(first_layer_size, inputs=35, activation="sigmoid"),
            NeuronLayer(10),
            NeuronLayer(1)
        ])

        min_error, errors, ii, training_accuracies, test_accuracies, min_error_test = perceptron.train(train_data, expected_data, test_data, expected_test, 2)
        #plot(ii, [training_accuracies, test_accuracies], ['train acc', 'test acc'], 'Epoch', 'Accuracies','Accuracies vs Epochs - multilayer')
        #plot(ii, [errors], ['errors'], 'Epoch', 'Errors', 'Mean Squared Error vs Epochs - multilayer')
        print("min error", min_error)
        print("min error test", min_error_test)
        print('training acc: ', len(training_accuracies))
        print('test accuracies: ', len(test_accuracies))
        plot_acc(ii,training=training_accuracies, test=test_accuracies) #Da cualquier cosa
        plot_list_error(errors)

        for j in range(len(to_train)):
            output = perceptron.predict(np.array(train_data[j]))
            #predictions.append(output)
            print(to_train[j], 'is ~', to_word(output[-1]))

        print() 
        print("TESTING")
        print("test", test_data)
        print("expected test", expected_test)
        print()

        for j in range(len(test_data)):
            output = perceptron.predict(np.array(test_data[j]))
            print(to_test[j], 'is ~', to_word(output[-1]))


def ex3_3():
    numbers = parseNumbers('./entries_3.txt')
    print('NUMBERS: ', np.array(numbers).shape)
    to_train = []
    train_data = []
    expected_data = []
    to_test = []
    test_data = []
    expected_test = []

    for i in range(10):
        to_train.append(i)
        train_data.append(numbers[to_train[i]])
        to_test.append(i)
        test_data.append(numbers[i])
    
    print('VS: ', test_data == train_data)
    train_data.append(numbers[:5])
    test_data.append(numbers[5:])

    for n in to_train:
        if n == 0:
            expected_data.append([1, -1, -1, -1, -1, -1, -1, -1, -1, -1])
        elif n == 1:
            expected_data.append([-1, 1, -1, -1, -1, -1, -1, -1, -1, -1])
        elif n == 2:
            expected_data.append([-1, -1, 1, -1, -1, -1, -1, -1, -1, -1])
        elif n == 3:
            expected_data.append([-1, -1, -1, 1, -1, -1, -1, -1, -1, -1])
        elif n == 4:
            expected_data.append([-1, -1, -1, -1, 1, -1, -1, -1, -1, -1])
        elif n == 5:
            expected_data.append([-1, -1, -1, -1, -1, 1, -1, -1, -1, -1])
        elif n == 6:
            expected_data.append([-1, -1, -1, -1, -1, -1, 1, -1, -1, -1])
        elif n == 7:
            expected_data.append([-1, -1, -1, -1, -1, -1, -1, 1, -1, -1])
        elif n == 8:
            expected_data.append([-1, -1, -1, -1, -1, -1, -1, -1, 1, -1])
        elif n == 9:
            expected_data.append([-1, -1, -1, -1, -1, -1, -1, -1, -1, 1])
        else:
            exit("error else ej 3")

    print("to train:", to_train)
    print()

    train_data = np.array(train_data)
    expected_data = np.array(expected_data)

    print('shape expected: ', expected_data.shape)
    perceptron = MultiLayerPerceptron([
        NeuronLayer(10, inputs=len(train_data[0]), activation="tanh"),
        NeuronLayer(10),
        NeuronLayer(expected_data.shape[1])
    ])

    for n in to_test:
        if n == 0:
            expected_test.append([1, -1, -1, -1, -1, -1, -1, -1, -1, -1])
        elif n == 1:
            expected_test.append([-1, 1, -1, -1, -1, -1, -1, -1, -1, -1])
        elif n == 2:
            expected_test.append([-1, -1, 1, -1, -1, -1, -1, -1, -1, -1])
        elif n == 3:
            expected_test.append([-1, -1, -1, 1, -1, -1, -1, -1, -1, -1])
        elif n == 4:
            expected_test.append([-1, -1, -1, -1, 1, -1, -1, -1, -1, -1])
        elif n == 5:
            expected_test.append([-1, -1, -1, -1, -1, 1, -1, -1, -1, -1])
        elif n == 6:
            expected_test.append([-1, -1, -1, -1, -1, -1, 1, -1, -1, -1])
        elif n == 7:
            expected_test.append([-1, -1, -1, -1, -1, -1, -1, 1, -1, -1])
        elif n == 8:
            expected_test.append([-1, -1, -1, -1, -1, -1, -1, -1, 1, -1])
        elif n == 9:
            expected_test.append([-1, -1, -1, -1, -1, -1, -1, -1, -1, 1])
        else:
            exit("error else ej 3")

    test_data = noise(test_data)

    min_error, errors, ii, training_accuracies, test_accuracies, min_error_test  = perceptron.train(train_data, expected_data, test_data, expected_test, 3)

    #plot(ii, [training_accuracies, test_accuracies], ['train acc', 'test acc'], 'Epoch', 'Accuracies', 'Accuracies vs Epochs - multilayer')
    #plot(ii, [errors], ['errors'], 'Epoch', 'Errors', 'Mean Squared Error vs Epochs - multilayer')
    print("training min error", min_error)
    print("testing min error", min_error_test)
    #print("Accuracies training", training_accuracies, "\nTest accuracies", test_accuracies)
    
    plot_acc(ii,training=training_accuracies,test=test_accuracies)
    plot_list_error(errors)
    for i in range(len(train_data)):
        output = perceptron.predict(np.array(train_data[i]))
        print(to_train[i], 'is ~', to_num(output))

    print()
    print("to test", to_test)
    print("test", test_data)
    print("expected test", expected_test)
    print()

    for i in range(len(test_data)):
        output = perceptron.predict(np.array(test_data[i]))

        print(to_test[i], 'is ~', to_num(output))

def to_num(array):
    aux = -math.inf
    num = 0
    for i in range(len(array)):
        if array[i] > aux:
            aux = array[i]
            num = i
    return num

def to_word(num):
    if num > 0:
        return "par " + str(num*100) + " %"
    elif num < 0:
        return "impar " + str(num*-100) + " %"
    else:
        return "wtf this shouldn't be printed"


def noise(array):
    for letter in array:
        for i in range(len(letter)):
            rand = random.uniform(0, 1)
            if rand <= 0.02:
                if letter[i] == 0:
                    letter[i] = 1
                elif letter[i] == 1:
                    letter[i] = 0
                else:
                    exit("error adding noise")
    return array

