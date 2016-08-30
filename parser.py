from pickle import load
import nltk


input = open('tagger.pkl', 'rb')
tagger = load(input)
input.close()


fp=open("sample.txt","r")

stopwords=open("stopwords.pkl","rb")
cachedStopWords = load(stopwords)
stopwords.close()

pattern  = '''FT: {<NN.*>+(<CC>?<AT>?<NN.*>)*(<IN><DT><NN.*>)?}
 OP: {(<JJ.*><,>?)+|<VBZ><D.*>?<JJ>|<\*>(<IN>|<ABN>|<AT>|<DT>|<QL>|<HV>|<A.*>)*(<JJ.*>|(<VB>|<VBG>|<VBD>|<VBN>)+|<AP>)|<VBG>(<IN>|<D.*>)*<JJ>?|(<VB>|<VBG>|<VBD>|<VBN>)}
 BR: {<CC>|<CS>|<W.*>|<IN>(<R.*>|<W.*>|<P.*>|<M.*>|<D.*>|<BE.*>|<Q.*>|<H.*>|<T.*>|<VB>)?}
 RT: {<R.*>|<P.*>|<M.*>|<D.*>|<BE.*>|<A.*>|<Q.*>|<IN>|<CC>|<H.*>|<T.*>|<NR>|<\*>|<CD>|<VBZ>|<U.*>}
 NP: {<FT><RT>*<OP>}'''

pattern2 ='''FT: {<NN.*>+(<CC>?<AT>?<NN.*>)*(<IN><DT><NN.*>)?}
 OP: {(<JJ.*><,>?)+|<VBZ><D.*>?<JJ>|<\*>(<IN>|<ABN>|<AT>|<DT>|<QL>|<HV>|<A.*>)*(<JJ.*>|(<VB>|<VBG>|<VBD>|<VBN>)+|<AP>)|<VBG>(<IN>|<D.*>)*<JJ>?|(<VB>|<VBG>|<VBD>|<VBN>)}
 BR: {<CC>|<CS>|<W.*>|<IN>(<R.*>|<W.*>|<P.*>|<M.*>|<D.*>|<BE.*>|<Q.*>|<H.*>|<T.*>|<VB>)?}
 RT: {<R.*>|<P.*>|<M.*>|<D.*>|<BE.*>|<A.*>|<Q.*>|<IN>|<CC>|<H.*>|<T.*>|<NR>|<\*>|<CD>|<VBZ>|<U.*>}
 NP: {<OP><RT>*<FT>}'''

chunker=nltk.RegexpParser(pattern)
chunker2=nltk.RegexpParser(pattern2)

NBclassifier=open('classifier.pkl',"rb")
classifier=load(NBclassifier)
NBclassifier.close()

def DisplayFeatures(feat, opinion, emotion):

    print feat,"\t\t\t",":","\t\t\t",opinion,"\t\t\t",":","\t\t\t",emotion,"\n\n"

    pass


def Classifier(opinion):

    return classifier.classify({"word": opinion})

def traverse(t):
    # t.draw()
    try:
        t.label()
    except AttributeError:
        print "Attribute Exception"
        return

    else:
        pos_tags=[]
        words=[]
        if t.label()=='NP':
            for child in t:
                pos_tags.append([pos for (word,pos) in child])
                words.append([word for (word,pos) in child])
                # print "child:",child
        else:
            for child in t:
                try:
                    if(child.label()=='NP'):
                        traverse(child)
                except Exception,e:
                    print e
                    continue
            return
    # print "POS Tags List :",pos_tags
    # print "Words List :",words
    flag=0
    flagB=0
    featureList=[]
    try :
        if(len(pos_tags)!=0 and len(words)!=0):
            cnt=0;
            feature=""

            for tag in pos_tags :
                count = 0
                taglen=len(tag)

                # print tag
                for tag in tag:
                    if tag == 'CC':
                        flag=1
                    if tag == 'NN' or tag == 'NNS' or tag == 'VBG':
                        try:
                                word=words[cnt][count]

                                if flag==0:
                                    if word not in cachedStopWords:
                                        feature=feature+word+" "
                                    if(count!=taglen-1 and flagB==0):
                                        if (pos_tags[cnt][count + 1] == 'NN' or pos_tags[cnt][count + 1] == 'NNS' or
                                                    pos_tags[cnt][count + 1] == 'VBG'):
                                            if words[cnt][count + 1] not in cachedStopWords:
                                                feature = feature + words[cnt][count + 1] + " "
                                        featureList.append(feature)
                                        flagB=1
                                    elif(flagB==0):
                                        featureList.append(feature)
                                elif flag==1:
                                    if word not in cachedStopWords:
                                        feature=word+" "
                                    if (count != taglen - 1 ):
                                        if(pos_tags[cnt][count+1]=='NN' or pos_tags[cnt][count+1]=='NNS' or pos_tags[cnt][count+1]=='VBG'):
                                            if words[cnt][count+1] not in cachedStopWords:
                                                feature = feature + words[cnt][count+1] + " "
                                    featureList.append(feature)
                                    flag=0
                                    flagB = 1
                                elif (flagB == 0):
                                    featureList.append(feature)
                        except Exception,e:
                            print("Feature concatenation exception:")+str(e)

                    count=count+1
                cnt=cnt+1

            cnt=0;
            opinion=""
            for des_tag in pos_tags :
                count = 0
                for des_tag in des_tag:
                    if des_tag == 'JJ' or des_tag == 'JJS' or des_tag == 'JJT' or des_tag == "*" or des_tag == 'JJR' or des_tag == 'VBZ' or des_tag == 'VB' or des_tag == 'VBD' or des_tag == 'VBG' or des_tag == 'VBN' or des_tag == 'VBP':
                        try:

                            word = words[cnt][count]
                            if word not in cachedStopWords:
                                opinion = opinion + word + " "
                        except:
                            print "Opinion concatenation exception"
                        # fp.write(" "+words[cnt]+" ")
                    count = count + 1
                cnt=cnt+1


            emotion=Classifier(opinion)
        if(len(opinion)!=0):
            for feat in featureList:
                if (feat!=""):
                    DisplayFeatures(feat,opinion,emotion)
    except:
        return


def display(str):
    sentences = nltk.sent_tokenize(str)
    sentences = [nltk.word_tokenize(sent) for sent in sentences] # NLTK word tokenizer
    sentences = [(tagger.tag(sent)) for sent in sentences]

    res=[]
    res2=[]

    try:
        for sent in sentences:
            res.append(chunker.parse(sent))
            res2.append(chunker2.parse(sent))
    except Exception,e:
        print "None Type Exception found in this review :",e.__str__()

    for r in res:
        # r.draw()
        traverse(r)
    for r in res2:
        # r.draw()
        traverse(r)


for line in fp:
    str = nltk.re.sub(" but ", " whereas ", line)
    str = nltk.re.sub(" with ", " ", str)
    display(str)
