import numpy as N

N_PTS = 10000

# Looping
def looping_solution():
    output = N.zeros(N_PTS)
    i = 0
    while i < N_PTS:
        # Generate random x values
        randInterval = N.random.uniform(low=0.0, high=1.0)
        randUpperBound = N.random.uniform(low=0.0, high=1.75) # or h=2.0
        if f(randInterval) > randUpperBound:
            output[i] = randInterval
            i = i + 1

    return output

def numpy_solution():
    output = N.zeros((0,))
    output_length = N.size(output)

    while output_length < N_PTS:
        randInterval = N.random.uniform(low=0.0, high=1.0,size=(N_PTS,))
        randUpperBound = N.random.uniform(low=0.0, high=1.75, size=(N_PTS,))

        temp = randIntervale[N.where( f(randIntervale) > randUpperBound)]
        output = N.concatenate([output, temp])
        output = output[0:N_PTS]
        output_length = N.size(output)


    return output

if __name__ == "__main__":

    print(looping_soution())
    print(numpy_solution())
