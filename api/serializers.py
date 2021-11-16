from rest_framework import serializers

class AnswerSerializer(serializers.Serializer):
    question = serializers.IntegerField()
    answer   = serializers.CharField()

class UserAnswersSerializer(serializers.Serializer):
    userId  = serializers.CharField()
    answers = AnswerSerializer(many=True)
    
class UserSerializer(serializers.Serializer):
    id          = serializers.CharField()
    surname     = serializers.CharField()
    rut         = serializers.CharField()
    courseId    = serializers.CharField()
    name        = serializers.CharField()
    perfil      = serializers.CharField()

class CollegeSerializer(serializers.Serializer):
    id      = serializers.CharField()
    dominio = serializers.CharField()
    name    = serializers.CharField()

class CourseSerializer(serializers.Serializer):
    id              = serializers.CharField()
    collegeId       = serializers.CharField()
    description     = serializers.CharField()
    nivel           = serializers.IntegerField()

class ExamSerializer(serializers.Serializer):
    id              = serializers.CharField()
    Alternativa     = serializers.IntegerField()
    Asignatura      = serializers.CharField()
    Nivel           = serializers.CharField()
    TipoEvaluacion  = serializers.CharField()
    level           = serializers.CharField()
    owner           = serializers.CharField()
    prueba          = serializers.CharField()
    state           = serializers.IntegerField()
    subject         = serializers.CharField()
    tipo            = serializers.CharField()

class AssigmentSerializer(serializers.Serializer):
    id          = serializers.CharField()
    Tipo        = serializers.CharField()
    courseId    = serializers.CharField()
    examId      = serializers.CharField()
    nombreExam  = serializers.CharField()
    state       = serializers.IntegerField()
    userId      = serializers.CharField() 

class QuestionSerializer(serializers.Serializer):
    id                  =   serializers.CharField()
    RespuestaA          =   serializers.CharField()
    RespuestaB          =   serializers.CharField()
    RespuestaC          =   serializers.CharField()
    RespuestaD          =   serializers.CharField()
    code                =   serializers.CharField()
    dominio             =   serializers.CharField()
    eje                 =   serializers.CharField()
    habilidad           =   serializers.CharField()
    idEvaluacion        =   serializers.CharField()
    ie                  =   serializers.CharField()
    level               =   serializers.CharField()
    oa                  =   serializers.CharField()
    order               =   serializers.CharField()
    owner               =   serializers.CharField()
    respuestaCorrecta   =   serializers.CharField()
    subject             =   serializers.CharField()
    textoPregunta       =   serializers.CharField()
    unidad              =   serializers.CharField()


