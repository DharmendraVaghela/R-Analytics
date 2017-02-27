import math,random,argparse

#input from the terminal
parser = argparse.ArgumentParser(description='Enter input values:')
parser.add_argument('--I_LMD', help='mean inter-arrival time',default=17.98,type = int)
parser.add_argument('--I_D',help = 'mean Re-transmission time',default=10,type = int)
parser.add_argument('--I_MU',help = 'service time',default=11,type = int)
parser.add_argument('--I_B',help = 'buffer size',default=5,type = int)
parser.add_argument('--I_NUM',help = 'Number of Repetitions',default=50,type = int)
args = parser.parse_args()

if args.I_LMD:
    LMD = args.I_LMD
if args.I_D:
    D = args.I_D
if args.I_MU:
    MU = args.I_MU
if args.I_B:
    B = args.I_B
if args.I_NUM:
    num = args.I_NUM

l = 0
output = []
while l < num:
    l += 1
    T_start = [0] * 1000
    D_start = [0] * 1000

    T_finish = [0] * 1000
    D_finish = [0] * 1000

    N = 0
    que = [] #id,st,et
    subq = []
    RetraT=0
    ArrivalT =0
    RAND_R = 0
    RAND_L = 0
    temp1 = 0
    devT = []
    retT = []
    sor1 = []
    sor2 = []
    Tp = 0
    Dp = 0
    while(N < 1000 or len(subq) >0):
        ArrivalT+= round(-1 * LMD * math.log(random.random()), 2)
        #if(N < 1000):
            #temp1 = numpy.random.poisson(LMD)
            #ArrivalT = ArrivalT + temp1
        RetraT = round(-1* D * math.log(random.random()), 2)
        #RetraT = RetraT + temp2
        if(N==0):
            T_start[N] = ArrivalT
            D_start[N] = 0
            D_finish[N] = 0
            T_finish[N] = ArrivalT + MU
            que.append((N,T_start[N],T_finish[N]))
        elif(N==1):
            T_start[N] = ArrivalT
            D_start[N] = 0
            D_finish[N] = 0
            T_finish[N] = T_finish[N-1] + MU
            que.append((N, T_start[N], T_finish[N]))
        else:
            if(len(que)>0):
                if(ArrivalT > que[0][2]):
                #T_finish[N] = que[0][2]
                    del que[0]
            #if (ArrivalT > que[0][2]):
                #del que[0]

            if(len(subq) > 0):
                for i, val in enumerate(subq):
                    if(ArrivalT > val[2]):
                        new = val[2]
                        while new < ArrivalT:
                            RetraT = round(-1 * D * math.log(random.random()), 2)
                            new+=RetraT
                        if(len(que) < B):
                            que.append((val[0],val[1],new+MU))
                            D_finish[val[0]] = new
                            T_finish[val[0]] = new+MU
                            del subq[i]
                        else:
                            subq.append((val[0],val[1],new+RetraT))
                            #D_finish[N] = val[2]+RetraT
                            del subq[i]

            if(N<1000):
                if(len(que) < B):
                    T_start[N] = ArrivalT
                    D_start[N] = 0
                    D_finish[N] = 0
                    if not (T_finish[N]):
                        #T_finish[N] = T_finish[N - 1] + MU
                        T_finish[N] = ArrivalT + MU
                    que.append((N, T_start[N], T_finish[N]))
                else:
                    T_start[N] = ArrivalT
                    D_start[N] = ArrivalT
                    subq.append((N, T_start[N], D_start[N] + RetraT))
            '''
            if(len(que) < B):
                T_start[N] = ArrivalT
                D_start[N] = 0
                D_finish[N] = 0
                if not(T_finish[N]):
                    T_finish[N] = T_finish[N - 1] + MU
                que.append((N, T_start[N], T_finish[N]))
            else:
                T_start[N] = ArrivalT
                D_start[N] = ArrivalT
                subq.append((N,T_start[N],D_start[N]+RetraT))'''
        N+=1

    devT = [round(a-b,2) for a,b in zip(T_finish,T_start)]
    retT = [round(a-b,2) for a,b in zip(D_finish,D_start)]

    P =0
    Tm = 0
    Dm = 0
    if(D_finish[999] > T_finish[999]):
        P = round(D_finish[999] - T_start[0],2)
    else:
        P = round(T_finish[999] - T_start[0],2)
    temp = [round(a-b,2) for a,b in zip(devT,retT)]
    Tm = round(sum(devT)/len(devT),2)
    Dm = round(sum(retT)/len(retT),2)
    sor1 = sorted(devT)
    Tp = sor1[949]
    sor2 = sorted(retT)
    k = math.ceil(0.95*(len(retT)))
    Dp = sor2[int(k-1)]
    output.append((Tm,Tp,Dm,Dp,P))

f = open('output_deliverable3.txt','w')
f.write('This run is with following values(All values can be changed from the input)\nMean inter-arrival time : 17.98\nMean retransmission time : 10\nBuffer size :'+str(B)+'\nNumber of Repititions : 50\n')
f.write('Service time : '+ str(MU)+'\n\n')
f.write('Repetition|Mean T|95th perc of T|Mean D|95th perc of D|P\n')
print 'Repetition|Mean T|95th perc of T|Mean D|95th perc of D|P'
i = 0
Tsum = sum(row[0] for row in output)
Tpsum = sum(row1[1] for row1 in output)
Dsum = sum(row2[2] for row2 in output)
Dpsum = sum(row3[3] for row3 in output)
Psum = sum(row4[4] for row4 in output)

Tsupermean = Tsum/num
Tpsupermean = Tpsum/num
Dsupermean = Dsum/num
Dpsupermean = Dpsum/num
Psupermean = Psum/num

Tinter = 0
Tpinter = 0
Dinter = 0
Dpinter = 0
Pinter = 0

while(i<len(output)):
    print (str(i+1)+'|'+str(output[i][0])+'|'+str(output[i][1])+'|'+str(output[i][2])+'|'+str(output[i][3])+'|'+str(output[i][4]))
    f.write (str(i + 1) + '|' + str(output[i][0]) + '|' + str(output[i][1]) + '|' + str(output[i][2]) + '|' + str(
        output[i][3]) + '|' + str(output[i][4])+'\n')
    Tinter+= (Tsupermean-output[i][0]) * (Tsupermean-output[i][0])
    Tpinter += (Tpsupermean - output[i][1]) * (Tpsupermean - output[i][1])
    Dinter+= (Dsupermean-output[i][2]) * (Dsupermean-output[i][2])
    Dpinter += (Dpsupermean - output[i][3]) * (Dpsupermean - output[i][3])
    Pinter += (Psupermean - output[i][4]) * (Psupermean - output[i][4])
    i+=1

Ts = math.sqrt(Tinter/num)
Tps = math.sqrt(Tpinter/num)
Ds = math.sqrt(Dinter/num)
Dps = math.sqrt(Dpinter/num)
Ps = math.sqrt(Pinter/num)

Tci = (Tsupermean-((1.96*Ts)/math.sqrt(num)),Tsupermean+((1.96*Ts)/math.sqrt(num)))
Tpci = (Tpsupermean-((1.96*Tps)/math.sqrt(num)),Tpsupermean+((1.96*Tps)/math.sqrt(num)))
Dci = (Dsupermean-((1.96*Ds)/math.sqrt(num)),Dsupermean+((1.96*Ds)/math.sqrt(num)))
Dpci = (Dpsupermean-((1.96*Dps)/math.sqrt(num)),Dpsupermean+((1.96*Dps)/math.sqrt(num)))
Pci = (Psupermean-((1.96*Ps)/math.sqrt(num)),Psupermean+((1.96*Ps)/math.sqrt(num)))

print ('\n')
print ('Grand Mean for T : '+str(Tsupermean))
print ('Confidence interval for T : '+str(Tci))
print ('Grand Mean for T_95 : '+str(Tpsupermean))
print ('Confidence interval for T_95 : '+str(Tpci))
print ('Grand Mean for D : '+str(Dsupermean))
print ('Confidence interval for D : '+str(Dci))
print ('Grand Mean for D_95 : '+str(Dpsupermean))
print ('Confidence interval for D_95 : '+str(Dpci))
print ('Grand Mean for P : '+str(Psupermean))
print ('Confidence interval for P : '+str(Pci))

f.write('\n')
f.write('Grand Mean for T : '+str(Tsupermean)+'\n')
f.write('Confidence interval for T : '+str(Tci)+'\n')
f.write('Grand Mean for T_95 : '+str(Tpsupermean)+'\n')
f.write('Confidence interval for T_95 : '+str(Tpci)+'\n')
f.write('Grand Mean for D : '+str(Dsupermean)+'\n')
f.write('Confidence interval for D : '+str(Dci)+'\n')
f.write('Grand Mean for D_95 : '+str(Dpsupermean)+'\n')
f.write('Confidence interval for D_95 : '+str(Dpci)+'\n')
f.write('Grand Mean for P : '+str(Psupermean)+'\n')
f.write('Confidence interval for P : '+str(Pci)+'\n')
f.close()