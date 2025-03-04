from Task2_mapper import getMedoids
def checkMedoids(medoids, medoids1):
    medoids_sorted = sorted(medoids)
    medoids1_sorted = sorted(medoids1)
    if medoids1_sorted == medoids_sorted:
        print(1)
    else:
        print(0)


if __name__ == "__main__":
    medoids = getMedoids('initialization.txt')
    medoids1 = getMedoids('initialization1.txt')
    
    checkMedoids(medoids, medoids1)