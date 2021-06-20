from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import http.client

from .rest.handlers import RestRequestHandler
from .forms import PredicatedCandidateForm, PredicatedCandidateFormBase64
from .scoring import scoring, read_pos_set, parts
from .image_decoder import decode_binary
from .utils import json_request_compat


class FacialScoringViewSet(RestRequestHandler):

    @csrf_exempt
    def rest_view(self, request, *args, **kwargs):
        return super().rest_view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        params = json_request_compat(request, method='POST')

        use_base64 = params.get('use_base64')
        use_base64 = use_base64 is not None and use_base64 == 'yes'

        if use_base64:
            form = PredicatedCandidateFormBase64(params)
        else:
            form = PredicatedCandidateForm(params, request.FILES)

        if not form.is_valid():
            return HttpResponse(status=http.client.BAD_REQUEST)

        images = {}

        for p in parts:
            images[p] = []

        img = decode_binary(form.cleaned_data['bimg'], form.cleaned_data['ext'], use_base64)

        for key, poses in read_pos_set(form.cleaned_data['pos_set']).items():
            for pos in poses:
                images[key].append(img[pos[1]:pos[1]+pos[3], pos[0]:pos[0]+pos[2]])

        return JsonResponse({
            'face': scoring(images['face']) if len(images['face']) > 0 else [],
            'eye': scoring(images['eye'], detector='eye') if len(images['eye']) > 0 else [],
            'nose': scoring(images['nose'], detector='nose') if len(images['nose']) > 0 else [],
            'mouth': scoring(images['mouth'], detector='mouth') if len(images['mouth']) > 0 else [],
        }, safe=False)
