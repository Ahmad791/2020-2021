# Code written in collaboration:
# Ahmad Wahbi 207417551
# Ernesto Evgeniy Sanches Shayda 

import sympy
import numpy as np
import matplotlib.pyplot as plt


def Caratheodory(P, u=None, dtype='float64'):
    ''' CARATHEODORY ALGORITHM taken verbatim from 
        "Fast and Accurate Least-Mean-Squares Solvers" 
        (NeurIPS19' - Oral presentation) 
         Alaa Maalouf and Ibrahim Jubran and Dan Feldman    
    '''
    """
    Implementation of the Caratheodory Theorem(1907)
    input: a numpy array P containing n rows (points), each of size d, and a positive vector of weights u (that sums to 1)
    output:a new vector of weights new_u that satisfies :
                1. new_u is positive and sums to 1
                2. new_u has at most d+1 non zero entries
                3. the weighted sum of P and u (input) is the same as the weighted sum of P and new_u (output)
    computation time: O(n^2d^2)
    """
    if u is None:
        u=np.ones(len(P))
    while 1:
        n = np.count_nonzero(u)
        d = P.shape[1]
        u_non_zero = np.nonzero(u)

        if n <= d + 1:
            return u

        A = P[u_non_zero]
        reduced_vec = np.outer(A[0], np.ones(A.shape[0]-1, dtype = dtype))
        A = A[1:].T - reduced_vec

        _, _, V = np.linalg.svd(A, full_matrices=True)
        v=V[-1]
        v = np.insert(v, [0],   -1 * np.sum(v))

        idx_good_alpha = np.nonzero(v > 0)
        alpha = np.min(u[u_non_zero][idx_good_alpha]/v[idx_good_alpha])

        w = np.zeros(u.shape[0] , dtype = dtype)
        tmp_w = u[u_non_zero] - alpha * v
        tmp_w[np.argmin(tmp_w)] = 0.0
        w[u_non_zero] = tmp_w
        w[u_non_zero][np.argmin(w[u_non_zero] )] = 0
        u = w
        
# HOMEWORK CODE FOR THREE VERSIONS OF THE CORESET   

def originalDist(data,X):
    ''' distance function '''
    result=[]
    for index,dataSet in enumerate(data):
        result.append([])
        for x in X:
            result[index].append(np.sum((dataSet-x)**2))
    return result

def calc_dist(point):
    ''' Euclidian distance '''
    return np.sqrt(np.sum(point ** 2))

def prepare_statistical_method(dataSet):
    ''' Calculating coreset using method 1 '''
    p=0
    px=0
    data_squared = dataSet ** 2
    px = np.sum(dataSet, axis=0)
    p = np.sum(data_squared)
    return [p,px]

def evaluate_on_coreset(dataSet, X, finalRes, p, px, n):
    ''' General function for finding error on the coreset '''
    for test in X:
        testDist=calc_dist(test)
        res=p+n*pow(testDist,2)-np.dot(test,px*2)
        finalRes[-1][-1].append(res) # adding the evaluation result
        #TODO: add the original result also


def firstQuest(data,X):
    ''' First method: coreset computation and evaluation '''
    finalRes=[]
    for index, dataSet in enumerate(data):
        temp=prepare_statistical_method(dataSet)
        p=temp[0]#sum of distances
        px=temp[1]#sum of distances and new point
        n=len(dataSet)
        finalRes.append([[p,px,n],[]])
        evaluate_on_coreset(dataSet, X, finalRes, p, px, n)
    return finalRes


def find_coreset_using_linear_algebra(A):
    ''' Second coreset method: computing the coreset '''
    theSum=np.sum(A,axis=0)
    linearly_independent_vectors_indexes=sympy.Matrix(A).T.rref()[1]
    B=A[list(linearly_independent_vectors_indexes)]# B are the linearly independent vectors
    weights=(theSum@np.linalg.inv(B))
    return (B, weights)

def find_coreset_using_caratheodory(A):
    ''' Third coreset method: computing the coreset '''
    weights = Caratheodory(A)
    non_zero_idx = (weights != 0)
    weights = weights[non_zero_idx]
    B = A[non_zero_idx]
    return (B, weights)
    
def prepare_A(dataSet):
    ''' Helper function to prepare the matrix for method 2 and 3 '''
    squares=np.sum(dataSet**2,axis=1, keepdims=True)
    ones=np.ones((len(squares),1))
    A=np.hstack((dataSet,squares, ones))
    return A
    
def prepare_linear_algebra_method(dataSet):
    ''' coreset computation: method 2 '''
    A = prepare_A(dataSet)
    return find_coreset_using_linear_algebra(A)

def prepare_caratheodory_method(dataSet):
    ''' coreset computation: method 3 '''
    A = prepare_A(dataSet)
    return find_coreset_using_caratheodory(A)
    
def second_and_third_Quest(data,X, coreset_f):
    ''' Generalized function for computing and evaluating methods 2 and 3 '''
    finalRes=[]
    for index,dataSet in enumerate(data):
        B, weights = coreset_f(dataSet)
        px = weights@(B[:, :-2])
        p = weights@(B[:, -2])
        n = weights@(B[:, -1])
        finalRes.append([[B, weights],[]])
        evaluate_on_coreset(dataSet, X, finalRes, p, px, n)
    return finalRes

def secondQuest(data,X):
    ''' Computing and evaluating method 2 '''
    return second_and_third_Quest(
        data, X, coreset_f=prepare_linear_algebra_method)

def thirdQuest(data,X):
    ''' Computing and evaluating method 3 '''
    return second_and_third_Quest(
        data, X, coreset_f=prepare_caratheodory_method)


if __name__=='__main__':
    data = [np.random.randint(-5000, 5000, (100 * i, 3)) for i in range(1, 11) ]
    X = np.random.randint(-10000, 10000, (100, 3))
    result=originalDist(data,X)
    coresets=[]#where to store the results, each cell contains the corsets and the test results of X
    coresets.append(firstQuest(data,X))
    coresets.append(secondQuest(data,X))
    coresets.append(thirdQuest(data,X))

    allTheMaxes=[[],[],[]]

    print("results are in:\n")
    for index0,coreset in enumerate(coresets):
        print("For coreset number "+str(index0)+":------------------------")
        for index1,dataSet in enumerate(data):
            print("for dataset number"+str(index1)+":")
            themax=0
            for index2,x in enumerate(result):
                themax=max(themax,(coreset[index1][1][index2]-result[index1][index2])/coreset[index1][1][index2])
            allTheMaxes[index0].append([len(dataSet),themax])
    
    plt.figure()
    plt.title("Coreset error comparison")
    plt.xlabel("data size")
    plt.ylabel("Error")
    for i, theMaxes in enumerate(allTheMaxes):
        sizes, costs  = zip(*theMaxes)
        plt.plot(sizes, costs, label="Method {}".format(i)) 
    plt.legend()
    plt.show()  
    
