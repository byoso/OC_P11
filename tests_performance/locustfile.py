#! /usr/bin/env python3
# coding: utf-8

from locust import HttpUser, task


class ProjectPerfTest(HttpUser):

    @task
    def index(self):
        self.client.get("/")

    @task
    def showSummary(self):
        self.client.get("/showSummary")
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get("/book/Spring Festival/Simply Lift")

    @task
    def purchasePlaces(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": 1
                }
            )

    @task
    def clubs_display(self):
        self.client.get('/clubs_display')

    @task
    def logout(self):
        self.client.get('/logout')
