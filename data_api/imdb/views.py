from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import  generics
from rest_framework.permissions import IsAuthenticated
from imdb.models import Movie, Actor, Director
from imdb.serializers import * 
from rest_framework import mixins
from django.views import View


#---CLASSICAL--------------------------------------------------------------------------------------------------------------

class MovieList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ActorList(mixins.ListModelMixin, generics.GenericAPIView):
    
    permission_classes = [IsAuthenticated]
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class ActorDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class DirectorList(generics.ListAPIView):
    
    permission_classes = [IsAuthenticated]
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class DirectorDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class GenreList(generics.ListAPIView):
    
    permission_classes = [IsAuthenticated]
    queryset = Genre.objects.values('name')
    serializer_class = GenresSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class GenreDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


#---EXERCICE/MANDATORY VIEWS-------------------------------------------------------------------------------------------------------------- 

class MovieRequest(View):

    permission_classes = [IsAuthenticated]

    
    def get(self, request, *args, **kwargs):
        if request.method == 'GET' :
            if 'date' in request.GET.keys():
                movies = Movie.objects.filter(year=request.GET['date'])
                serializer = MovieSerializer(movies, many=True)
            elif 'title' in request.GET.keys():
                movies = Movie.objects.filter(titre=request.GET['title'])
                serializer = MovieSerializer(movies, many=True)
            else:
                return JsonResponse({"Errmessage":"query parameter do not object any of the object's fields"},safe=True, status=200)
            
            return JsonResponse(serializer.data, safe=False, status=200)
        else : 
            return JsonResponse({'message':'BAD HTTP METHOD'})



#---LEGACY CONTENT ---------------------------------------------------------------------------------------------------
# class ScenaristList(generics.ListCreateAPIView, 
#                 mixins.ListModelMixin, 
#                 mixins.CreateModelMixin):
    
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     queryset = Scenarist.objects.all()
#     serializer_class = ScenaristSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

# class ScenaristDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     queryset = Scenarist.objects.all()
#     serializer_class = ScenaristSerializer

# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
############################################################################################
# OTHER METHODS : 
# 
# -- Classic --------------------------------------------------------------
# @csrf_exempt
# @api_view(['GET','POST'])
# def movies_list(request, format=None):
#     """
#     List all code movies, or create a new movie.
#     """

#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
        
#         serializer = MovieSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
        
#         return JsonResponse(serializer.errors, status=400)
    

# @csrf_exempt
# @api_view(['GET','PUT','DELETE'])
# def movie_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a code movie.
#     """
#     try:
#         movie = Movie.objects.get(pk=pk)
#     except Movie.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = MovieSerializer(movie)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = MovieSerializer(movie, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         movie.delete()
#         return HttpResponse(status=204)
#
#
# ------------Mixins based -------------------------------------------------------------------
# just change the object name
#
# from rest_framework import mixins
# 
# class SnippetList(mixins.ListModelMixin,
    #               mixins.CreateModelMixin,
    #               generics.GenericAPIView):
    # queryset = Snippet.objects.all()
    # serializer_class = SnippetSerializer

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)