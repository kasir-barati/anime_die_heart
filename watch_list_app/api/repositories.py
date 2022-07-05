from ..models import Movie


class MovieRepository:
    def find_by_id(self, id: int,) -> Movie:
        movie = Movie.objects.get(pk=id)
        return movie

    # TODO: Annotate return type if possible
    def find_all(self,):
        return Movie.objects.all()

    def update_by_id(self, id: int, movie: Movie,) -> Movie:
        movie = Movie.objects.filter(pk=id).update(
            name=movie.name,
            description=movie.description,
            active=movie.active
        )
        return movie

    def delete_by_id(self, id: int,) -> Movie:
        # TODO: I am not sure if this will throw error if record does not exists
        # BTW I will try it. If it won't throw error
        movie = Movie.objects.filter(pk=id).delete()
        return movie

        

