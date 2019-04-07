package ru.zinin.mylibrary.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import ru.zinin.mylibrary.repos.UserRepo;

@Controller
@RequestMapping("/user")
public class UserController {

    @Autowired
    UserRepo userRepo;

    @GetMapping
    public String userList(Model model) {
        model.addAttribute("users", userRepo.findAll());
        return "user_list";
    }
}
