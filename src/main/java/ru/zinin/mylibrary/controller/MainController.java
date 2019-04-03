package ru.zinin.mylibrary.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import ru.zinin.mylibrary.domain.Book;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

@Controller
public class MainController {

    @GetMapping
    public String homePage(Model model) {
        return "home_page";
    }

    @GetMapping("/test")
    public String test(Model model) {
        return "test";
    }


    @GetMapping("/main")
    public String main(Model model) {
        List<Book> books = new ArrayList<Book>() {{
            add(new Book("Дабог","Головачев"));
            add(new Book("Мать","Горький"));
            add(new Book("Как закалялась сталь","Островский"));
        }};
        model.addAttribute("books", books);
        return "main";
    }

}
