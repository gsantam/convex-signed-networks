import sys

parametersFile = file("comm_params.txt","r")
actualLine = parametersFile.readlines()[int(sys.argv[1])]
actualLine = actualLine.strip()
numberOfCommunities = actualLine.split("\t")[0]

communitiesFile = file("/homedtic/gsantamaria/home/Tesis/psl/psl-example/data/sn/sn_communities.txt","w")
communitiesFile.truncate()
first = True

for i in range(int(numberOfCommunities)):
  if first == True:
    first = False
  else:
    communitiesFile.write("\n")
  communitiesFile.write(str(i))
communitiesFile.close()

firstVerticesFile = file("/homedtic/gsantamaria/home/Tesis/psl/psl-example/data/sn/sn_first_vertex.txt","w")
firstVerticesFile.truncate()

firstVertices = actualLine.split("\t")[1]
first=True
for ind,vertex in enumerate(firstVertices.split(" ")):
  if first == True:
    first = False
  else:
    firstVerticesFile.write("\n")
  firstVerticesFile.write(str(vertex))
  firstVerticesFile.write(str("\t"))
  firstVerticesFile.write(str(ind))
